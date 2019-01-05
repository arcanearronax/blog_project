from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404
from .models import *

def index(request):
	posts = Post.objects.order_by('pub_date')
	template = loader.get_template('index.html')
	context = {
		'posts': posts,
	}
	return HttpResponse(template.render(context, request))

def blog(request):
	return HttpResponse('<h2>Blog Homepage</h2>')

def blogPost(request, cat_desc, id):
	# Get the post we're looking at
	post = get_object_or_404(Post, pk=id)
	# Get the info for other posts
	cat_id = get_object_or_404(Category, pk=post.cat_id)
	recent = get_object_or_404(Post, cat_id=cat_id)
	template = loader.get_template('blog_post.html')
	context = {
		'post': post,
		'cat_desc': cat_desc,
		'recent_posts': recent[:5],
	}
	return HttpResponse(template.render(context, request))

def categoryHome(request, desc):
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
