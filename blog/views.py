from django.shortcuts import render
from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from django.shortcuts import redirect#redirect users to whatever page they want
from django.contrib.auth import authenticate, login
from django.views.generic import View
from .forms import UserForm, PostForm
from django.views import generic
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.core.context_processors import csrf
from django.conf import settings
from django import http
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,Http404,HttpResponseRedirect


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


#------------------------------------------------------------------
class Indexview(generic.ListView):
    template_name = 'templates/blog/post_list.html'

    def get_queryset(self):  #we can search 4 the reqd items in DB
        return Post.objects.all()



class DetailView(generic.DetailView):
    model=Post
    template_name = 'blog/post_detail.html'


class PostCreate(CreateView):
    model=Post
    fields=['author','title','text']

class PostUpdate(UpdateView):
    model=Post
    fields=['author','title','text']

class PostDelete(DeleteView):
    model=Post
    success_url = reverse_lazy('blog:post_list')



class BlockedIPMiddleware(object):
    def process_request(self, request):
        if request.META['REMOTE_ADDR'] in settings.BLOCKED_IPS:
            return http.HttpResponseForbidden('<h1>Forbidden</h1>')
        return None




def add_comment(request,pk):
    """
    comments = Comment.objects.order_by('created_date')
    #.filter(created_date__lte=timezone.now())
    return render(request,'blog/comments.html',{'comments':comments})
    """
    post=get_object_or_404(Post,pk=pk)
    if request.method == 'POST':
        form=CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('blog.views.post_detail',pk=post.pk)
    else:
        form = CommentForm()

    return render(request, 'blog/comments.html', {'form': form})



#----------------------------------------------------------

#UserForm is the Form blueprint we created in forms.py
#View in bracket means userformview inherits from view
class UserFormView(View):
    form_class=UserForm
    template_name="blog/registration_form.html"

    #display blank form
    def get(self,request):
        form=self.form_class(None)
        return render(request.self.template_name,{'form':form})
#process form data when user has to submit
    def post(self,request):
        form=self.form_class(request.POST)#req.Post means the info passed to the form
        if form.is_valid():
#creates an obj but doesnt save it to db
            user=form.save(commit=False)
#cleaned normalized data
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
#to chnge user passwrd
            user.set_password(password)
            user.save()
            user=authenticate(username=username,password=password)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect('blog:post_list')
        return render(request.self.template_name,{'form':form})







def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)


        if user is not None:
            if user.is_active:
                login(request, user)
                posts = Post.objects.filter(user=request.author)
                #after they login we want to redirect them to homepg
                return render(request, 'blog/post_list.html', {'posts': posts})
            #if the din login, return that try again->here is a blank form for u
        return render(request.self.template_name,{'form':form})


    context = {
        "form": form,
    }
    return render(request, 'blog/registration_form.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                #login(request, user)
                posts = Post.objects.all()
                return render(request, 'blog/post_list.html', {'posts': posts})
            else:
                return render(request, 'blog/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'blog/login.html', {'error_message': 'Invalid login'})
    return render(request, 'blog/login.html')


@login_required
def post_publish(request, pk):
    post=get_object_or_404(Post, pk=pk)
    post.publish()
    messages.success(request, "Post successfully published!")
    return redirect('blog.views.post_detail', pk=pk) #return redirect('blog.views.post_detail', pk=pk)


@login_required
def post_draft_list(request):
    posts=Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request,'blog/post_draft_list.html',{'posts':posts})

@login_required
def post_remove(request,pk):
    post=get_object_or_404(Post,pk=pk)
    post.delete()
    #messages.success(request, "Post was successfully deleted!")
    return redirect('blog.views.post_list')