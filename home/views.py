from django.shortcuts import render, redirect, get_object_or_404
from .form import UserRegisterForm,Contant,ProfileUpdateForm,UserUpdateForm,CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ( 
            ListView, 
            DetailView,
            CreateView,
            UpdateView,
            DeleteView
            
)
from django.contrib.auth import get_user_model
from .models import Blog,Comment,Wiseword
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
def home(request):
   # contant = get_object_or_404(Menu, id=id)
    if request.method == 'POST':
        c_form = Contant(request.POST )
        if  c_form.is_valid():
            c_form.save()        
            messages.success(request, f'You have successfully sent the message')
            
            return redirect('home')

    else:
        
        c_form = Contant()
    User = get_user_model()
    users = len(User.objects.all())
    context = {
        'c_form' : c_form,
        'words' : Wiseword.objects.all(),
        'members': users
        
    }
    return render(request, 'home/index.html', context)

def blog(request):
    blogs = Blog.objects.all()
    context= {
        'blogs':blogs
    }
    return render(request, 'home/blog.html', context)

class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    #template_name ='home/blog_create.html'
    fields = ['the_photo', 'title', 'content']
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Blog
    fields = ['the_photo', 'title', 'content']
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Blog 
    template_name='home/blog_confirm_delete.html'
    success_url = '/'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def team(request):
    User = get_user_model()
    users = User.objects.all()
    context={
        'users':users
    }
    return render(request, 'home/team.html', context)


class WiseCreateView(LoginRequiredMixin, CreateView):
    model = Wiseword
    template_name='home/wiseform.html'
    fields = ['the_words']
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    template_name ='home/blog_detail.html'
    fields = ['code', 'message']
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
def blog_single(request, id=None):
    blog = get_object_or_404(Blog, id=id)
    messages = ''
    if request.method == 'POST':
        form = CommentForm(request.POST, None)
        if form.is_valid():
            obj = form.save( commit = False)
            obj.author = request.user
            obj.save()
            form = CommentForm()
            redirect('blog-single', id)
            
            
    else:
        form = CommentForm()#the brackets to create a new instance
    
    context = {
        messages: f'You have successfully commented',
        'form' : form,
        'comments': Comment.objects.filter(code=id).order_by('-date_posted'),
        'comment':len(Comment.objects.filter(code=id)),
        'code': id,
        'blog':blog
    }
    return render(request, 'home/blog_detail.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been created! You can now Login')
            return redirect('login')#this is to take us back to the home page after form is valid
    else:
        form = UserRegisterForm()#the brackets to create a new instance
    return render(request, 'home/register.html', {'form' : form})

@login_required#apear only when a user is loged in
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account have been successfully updated')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form' : u_form,
        'p_form' : p_form
    }
    return render(request, 'home/profile.html', context)




