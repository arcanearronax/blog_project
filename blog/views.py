from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, reverse
from .models import *
from .forms import PostForm, CatForm
import logging
from django.utils.html import escape

logger = logging.getLogger(__name__)

def blogHome(request):
	categories = Category.getCategories()
	template = loader.get_template('blog_home.html')

	#posts = Post.objects.order_by('-pub_date')
	posts = Post.getPosts(order='pub_date', reverse=1)

	recent_posts = [(post, categories.get(pk=post.cat.id)) for post in posts[:5]]

	cnt = posts.count()

	context = {
		'cnt': cnt,
		'recent_posts': recent_posts,
		'cats': categories,
		'categories': categories,
	}

	return HttpResponse(template.render(context, request))

def blogLogin(request):
	template = loader.get_template('blog_login.html')
	context = {}
	return HttpResponse(template.render(context, request))

def blogLogout(request):
	return HttpResponse('Blog Logout Page')

def blogAdmin(request):
	logger.info('Enter blogAdmin')

	if request.method == 'POST':

		if 'NewPost' in request.POST:
			form = PostForm(request.POST)
			if form.is_valid():
				post = form.save(commit=False)
				post.title = request.POST.get('title')
				post.cat = get_object_or_404(Category, pk=int(request.POST.get('cat')))
				post.text = request.POST.get('text')
				post.id = Post.objects.count() + 1
				post.save()
				return redirect('/blog/{}/{}'.format(post.cat.desc, post.id))
			else:
				return HttpResponse('Invalid Post Form')
		elif 'NewCategory' in request.POST:
			form = CatForm(request.POST)
			if form.is_valid():
				post = form.save(commit=False)
				post.desc = request.POST.get('desc')
				if (request.POST.get('hide') == 'on'):
					post.hide = True
				else:
					post.hide = False
				post.id = Category.objects.count() + 1
				post.save()
				return redirect('/blog/{}'.format(post.desc))
			else:
				return HttpResponse('Invalid Cat Form')
		else:
			return HttpResponse(request.POST)

	pForm = PostForm()
	cForm = CatForm()

	template = loader.get_template('blog_admin.html')
	cat_descs = Category.getCategories(hidden=1)
	context = {
		'cat_descs': cat_descs,
		'pForm': pForm,
		'cForm': cForm,
	}
	return HttpResponse(template.render(context, request))

def blogError(request):
	return HttpResponse('You got an error.')

def categoryHome(request, desc):
	id = get_object_or_404(Category, desc=desc).id
	posts = Post.objects.filter(cat=id).order_by('pub_date')
	#posts = Post.getPosts(order='pub_date')
	cnt = posts.count()
	template = loader.get_template('blog_page.html')
	context = {
		'posts': posts[:5],
		'cnt': cnt,
		'desc': desc,
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

def newPost(request):
	form = PostForm(request.post)
	if (form.isValid()):
		post = form.save(commit=False)
		post.title = request.title
		post.cat_id = get_object_or_404(Category, desc=request.cat_desc).id
		post.text = request.desc
		post.save
	return redirect('blog_admin.py')

def blogTest(request):
	cats = Category.getCategories()
	template = loader.get_template('base_home.html')

	context = {
		'cats': cats,
	}

	return HttpResponse(template.render(context, request))
