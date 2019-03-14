from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, reverse
from .models import *
from .forms import PostForm, CatForm
import logging
from django.utils.html import escape

logger = logging.getLogger(__name__)

def blogHome(request):
	cats = Category.getCategories()
	template = loader.get_template('blog_home.html')
	Post.getPosts().count()
	post = Post.getPosts(post_id=Post.getPosts().count())

	context = {
		'cats': cats,
		'post': post,
	}

	return HttpResponse(template.render(context, request))

def categoryHome(request, desc):
	template = loader.get_template('blog_category.html')

	cat = get_object_or_404(Category, desc=desc)
	posts = Post.getPosts(cat=cat, hidden=1)
	try:
		post = posts[0]
	except:
		post = ''

	context = {
		'posts': posts,
		'cat': cat,
		'post': post,
	}

	return HttpResponse(template.render(context, request))

def blogPost(request, desc, id):
	template = loader.get_template('blog_post.html')

	cat = get_object_or_404(Category, desc=desc)
	posts = Post.getPosts(id=id)

	context = {
		'posts': posts,
		'cat': cat,
	}
	return HttpResponse(template.render(context, request))

def blogAdmin(request):
	logger.info('Enter blogAdmin')
	if request.method == 'POST':
		if 'PostReq' in request.POST:
			form = PostForm(request.POST)
			if form.is_valid():
				post = form.save(commit=False)
				post.title = request.POST.get('title')
				post.cat = get_object_or_404(Category, pk=int(request.POST.get('cat')))
				post.text = request.POST.get('text')
				#return HttpResponse(post.cat)
				try:
					temp_id = request.POST.get('post_id')
				except e:
					#return HttpResponse(e)
					post.id = Post.objects.count() + 1
				post.save()
				return redirect('/blog/{}/{}'.format(post.cat.desc, post.id))
			else:
				return HttpResponse(form.errors)
		elif 'CatReq' in request.POST:
			form = CatForm(request.POST)
			if form.is_valid():
				post = form.save(commit=False)
				post.desc = request.POST.get('desc')
				if (request.POST.get('hide') == 'on'):
					post.hide = True
				else:
					post.hide = False
				post.id = request.POST.get('cat_id')
				if (post.id == -1):
					post.id = Category.objects.count() + 1
				post.save()
				return redirect('/blog/{}'.format(post.desc))
			else:
				return HttpResponse('Fail 1 - {}'.format(request.POST))
		else:
			return HttpResponse('Fail 2 - {}'.format(request.POST))

	template = loader.get_template('blog_admin.html')
	cats = Category.getCategories(hidden=1)
	posts = Post.getPosts(hidden=1)

	pForm = PostForm()
	pForm.id = -1
	cForm = CatForm()
	cForm.id = -1

	context = {
		'cats': cats,
		'posts': posts,
		'pcnt': posts.count(),
		'ccnt': cats.count(),
		'post_json': Post.get_json(),
		'cat_json': Category.get_json(),
		'pForm': pForm,
		'cForm': cForm,
	}

	return HttpResponse(template.render(context, request))

# Using this to test new features
def blogTest(request):
	template = loader.get_template('blog_test.html')
	cats = Category.getCategories(hidden=1)
	posts = Post.getPosts(hidden=1)

	pForm = PostForm()
	pForm.id = -1
	cForm = CatForm()
	cForm.id = -1

	context = {
		'cats': cats,
		'posts': posts,
		'pcnt': posts.count(),
		'ccnt': cats.count(),
		'post_json': Post.get_json(),
		'cat_json': Category.get_json(),
		'pForm': pForm,
		'cForm': cForm,
	}
	return HttpResponse(template.render(context, request))

def blogError(request):
	return HttpResponse('You got an error.')

def blogLogin(request):
	template = loader.get_template('blog_login.html')
	context = {}
	return HttpResponse(template.render(context, request))

def blogLogout(request):
	return HttpResponse('Blog Logout Page')
