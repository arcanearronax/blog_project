from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, reverse
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

def debugPage(request, title):
	template = loader.get_template('debug_page.html')
	context = {
		'title': title,
	}
	return HttpResponse(template.render(context, request))

def blogAdmin(request):
	logger.info('Enter blogAdmin')

	print(request.method)

	if request.method == 'POST':
		form = PostForm(request.POST)

		if form.is_valid():
			post = form.save(commit=False)
			post.title = request.POST.get('title')
			post.cat = get_object_or_404(Category, pk=int(request.POST.get('cat')))
			post.text = request.POST.get('text')

			post.id = Post.objects.count() + 1

			post.save()
			return redirect('/blog/{}/{}'.format(post.cat.desc, post.id))

			#return redirect('blogPostById', cat_desc=request.cat_desc, id=post.pk)
			#return HttpResponse(loader.get_template({'title': 'SUCCESS',}, request))
			#return debugPage(request, 'OOPS')
		#else:
			#return redirect('../error')
			#print(form.errors)
			#return debugPage(request, form.errors)

	form = PostForm()

	template = loader.get_template('blog_admin.html')
	cat_descs = Category.objects.order_by('id')
	context = {
		'cat_descs': cat_descs,
		'form': form,
	}
	return HttpResponse(template.render(context, request))

def blogPost(request, cat_desc, id):
	# Get the post we're looking at
	post = get_object_or_404(Post, pk=id)
	# Get the info for other posts
	cat_desc = get_object_or_404(Category, pk=post.cat_id)
	recent = Post.objects.filter(cat=post.cat_id)
	template = loader.get_template('blog_post.html')
	cnt = recent.count()
	context = {
		'post': post,
		'desc': cat_desc,
		'cnt': cnt,
		'recent_posts': recent[:5],
	}
	return HttpResponse(template.render(context, request))

def categoryHome(request, desc):
	#if (desc == 'admin'):
	#	return blogAdmin(request)
	id = get_object_or_404(Category, desc=desc).id
	posts = Post.objects.filter(cat=id).order_by('pub_date')
	cnt = posts.count()
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

def blogHome(request):
	categories = Category.objects.order_by('id')
	template = loader.get_template('blog_home.html')

	context = {
		'categories': categories
	}

	return HttpResponse(template.render(context, request))

def blogLogin(request):
	return HttpResponse('Do this later.')
