from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (
					TemplateView, ListView,
					DetailView, CreateView,
					UpdateView, DeleteView
)
from django.utils import timezone
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from blog.models import Post, Comment
from blog.forms import PostForm, CommentForm
from django.contrib.auth.models import User
#register imports
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

#change password imports
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

# Create your views here.

class AboutView(TemplateView):
	template_name = 'about.html'

class PostListView(ListView):

	model = Post

	def get_queryset(self):
		return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

		# -published_date refers to decending order of blog list order by published_date
		# __lte is a lookup type equivalent of less then or equal.

class PostDetailView(DetailView):
	model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
	login_url = '/account/login/'
	redirect_field_name = 'blog/post_detail.html'
	form_class=PostForm
	model = Post

	def form_valid(self, form):
		form.instance.auther = self.request.user
		return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
	login_url = '/account/login/'
	redirect_field_name = 'blog/post_detail.html'
	form_class=PostForm
	model = Post

class PostDeleteView(LoginRequiredMixin, DeleteView):
	login_url = '/account/login/'
	model = Post
	success_url = reverse_lazy('blog:post_list')

class DraftListView(LoginRequiredMixin, ListView):
	login_url = '/account/login/'
	template_name = 'blog/draft_list.html'
	context_object_name = 'draft_list'
	#redirect_field_name = 'blog/draft_list.html'
	model = Post

	def get_queryset(self):
		return Post.objects.filter(published_date__isnull=True).order_by('create_date')

########################################################
########################################################

@login_required(login_url='/account/login/')
def post_publish(request, pk):
	post = get_object_or_404(Post, pk=pk)
	post.publish()
	return redirect('blog:post_detail', pk=pk)

@login_required(login_url='/account/login/')
def post_unpublish(request, pk):
	Post.objects.filter(id=pk).update(published_date=None)
	return redirect('blog:post_detail', pk=pk)

@login_required(login_url='/account/login/')
def add_comment_to_post(request, pk):
	post = get_object_or_404(Post, pk=pk)

	if request.method=='POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			form.instance.viewer = request.user
			comment.post = post
			comment.save()
			return redirect("blog:post_detail", pk=post.pk)
	else:
		form = CommentForm()
		return render(request, 'blog/comment_form.html', {'form':form})

@login_required(login_url='/account/login/')
def comment_approve(request, pk):
	comment = get_object_or_404(Comment, pk=pk)
	comment.approve()
	return redirect('blog:post_detail', pk=comment.post.pk)

@login_required(login_url='/account/login/')
def comment_delete(request, pk):
	comment = get_object_or_404(Comment, pk=pk)
	post_pk = comment.post.pk
	comment.delete() #delete in django built-in method to delete the object
	return redirect('blog:post_detail', pk=post_pk)

def register(request):

	if request.method=='POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			messages.success(request,'You are registered succesffully')
			return redirect('/')
		else:
			messages.error(request, 'Please correct the error below.')
			return render(request, 'registration/register.html', {'form':form})

	else:
		form =UserCreationForm()
		return render(request, 'registration/register.html', {'form':form})

@login_required(login_url='/account/login/')
def change_password(request):

	if request.method == 'POST':
		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user) #importent
			"""
			Call update_session_auth_hash() after saving the form.
			Otherwise the user’s auth session will be invalidated 
			and she/he will have to log in again.
			"""
			messages.success(request, 'Your password is successfully updated! Login again to continue.')
			logout(request)
			return redirect('/account/login/')
		else:
			messages.error(request, 'Please correct the error below.')
			return render(request, 'registration/change_password.html', {'form':form})
	else:
		form = PasswordChangeForm(request.user)
		return render(request, 'registration/change_password.html', {'form':form})

