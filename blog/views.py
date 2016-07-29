from django.shortcuts import render
from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from django.shortcuts import redirect#redirect users to whatever page they want
from django.contrib.auth import authenticate, login
from django.views.generic import View
from .forms import UserForm
from django.views import generic
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView,UpdateView,DeleteView

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







