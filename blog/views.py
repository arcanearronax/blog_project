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
	cats = Category.getCategories()
	template = loader.get_template('blog_home.html')
	post = Post.getPosts(id=Post.getPosts().count())

	context = {
		'cats': cats,
		'post': post[0],
	}

	return HttpResponse(template.render(context, request))

def categoryHome(request, desc):
	template = loader.get_template('blog_category.html')

	cat = get_object_or_404(Category, desc=desc)
	posts = Post.getPosts(cat=cat)
	context = {
		'posts': posts,
		'cat': cat,
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

def blogLogin(request):
	template = loader.get_template('blog_login.html')
	context = {}
	return HttpResponse(template.render(context, request))

def blogLogout(request):
	return HttpResponse('Blog Logout Page')
