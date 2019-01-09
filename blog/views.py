from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from .models import *
from .forms import PostForm
import logging
from django.utils.html import escape

logger = logging.getLogger(__name__)

def blogPostById(request, post_id):
	post = get_object_or_404(Post, pk=post_id)
	cat_desc = get_object_or_404(Category, pk=post.cat)
	return blogPost(request, cat_desc=cat_desc, id=post_id)

def index(request):
	posts = Post.objects.order_by('pub_date')
	template = loader.get_template('index.html')
	context = {
		'posts': posts,
	}
	return HttpResponse(template.render(context, request))

def blogAdmin(request):
	logger.info('Enter blogAdmin')

	print(request.method)

	if request.method == 'POST':
		form = PostForm(request.POST)

		if form.is_valid():
			blogpost = form.save(commit=False)
			blogpost.title = request.title
			blogpost.cat = get_object_or_404(Category, desc=request.cat_desc).id
			blogpost.text = request.desc
			blogpost.save()

			return redirect('blogPostById', cat_desc=request.cat_desc, id=blogpost.pk)
		else:
			#return redirect('../error')
			print(form.errors)
			return HttpResponse(escape(repr(request)))

	template = loader.get_template('blog_admin.html')
	cat_descs = Category.objects.order_by('id')
	context = {
		'cat_descs': cat_descs,
	}
	return HttpResponse(template.render(context, request))

def blogPost(request, cat_desc, id):
	# Get the post we're looking at
	post = get_object_or_404(Post, pk=id)
	# Get the info for other posts
	cat_desc = get_object_or_404(Category, pk=post.cat_id)
	recent = get_object_or_404(Post, cat=post.cat_id)
	template = loader.get_template('blog_post.html')
	context = {
		'post': post,
		'desc': cat_desc,
		'recent_posts': recent[:5],
	}
	return HttpResponse(template.render(context, request))

def categoryHome(request, desc):
	if (desc == 'admin'):
		return blogAdmin(request)
	id = get_object_or_404(Category, desc=desc).id
	posts = Post.objects.filter(cat=id).order_by('pub_date')
	cnt = 2
	template = loader.get_template('blog_page.html')
	context = {
		'posts': posts[:5],
		'cnt': cnt,
		'desc': desc,
	}
	return HttpResponse(template.render(context, request))

def categoryAdmin(request, desc):
	return

def newPost(request):
	form = PostForm(request.post)
	if (form.isValid()):
		post = form.save(commit=False)
		post.title = request.title
		post.cat_id = get_object_or_404(Category, desc=request.cat_desc).id
		post.text = request.desc
		post.save
	return redirect('blog_admin.py')

def blogError(request):
	return HttpResponse('You got an error.')
