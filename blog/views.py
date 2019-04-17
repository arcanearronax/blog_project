from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, reverse
from .models import *
from .forms import PostForm, CatForm, LoginForm
import logging
from django.utils.html import escape
from django.core import serializers
from django.contrib.auth import authenticate, login, logout

logger = logging.getLogger(__name__)

def blogHome(request):
	cats = Category.getCategories()
	template = loader.get_template('blog_home.html')
	post = Post.objects.get(post_id=int(Post.getPosts().count()))

	context = {
		'cats': cats,
		'post': post,
	}

	return HttpResponse(template.render(context, request))

def categoryHome(request, desc):
	template = loader.get_template('blog_category.html')

	cat = get_object_or_404(Category, desc=desc)
	posts = Post.getPosts(cat_id=cat.cat_id, hidden=1)
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
	post = Post.getPosts(post_id=id)

	context = {
		'post': post,
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
				post.post_id = Post.objects.count() + 1
				post.title = request.POST.get('title')
				post.cat_id = Category.getCategories(cat_id=int(request.POST.get('cat_id')))
				post.text = request.POST.get('text')
				post.save()
				return redirect('/blog/{}/{}'.format(post.cat_id.desc, post.post_id))
			else:
				# Really need to change how I handle this
				try:
					#return HttpResponse('Fail-5')
					post = Post.objects.get(post_id=int(request.POST.get('post_id'))+1)
					post.title = request.POST.get('title')
					post.cat_id = Category.getCategories(cat_id=int(request.POST.get('cat_id')))
					post.text = request.POST.get('text')
					post.save(update_fields=['title','cat_id','text'])
					return redirect('/blog/{}/{}'.format(post.cat_id.desc, post.post_id))
				except Exception as e:
					return HttpResponse('<p>Invalid Post - {}</p>'.format(form.errors.as_text))
				else:
					return HttpResponse('Unknown Post Error')

		elif 'CatReq' in request.POST:
			form = CatForm(request.POST)
			if form.is_valid():
				cat = form.save(commit=False)
				cat.cat_id = Category.objects.count() + 1
				cat.desc = request.POST.get('desc')
				if (request.POST.get('hide') == 'on'):
					cat.hide = True
				else:
					cat.hide = False
				cat.save()
				return redirect('/blog/{}'.format(cat.desc))
			else:
				try:
					cat = Category.objects.get(cat_id=int(request.POST.get('cat_id'))+1)
					cat.desc = request.POST.get('desc')
					if (request.POST.get('hide') == 'on'):
						cat.hide = True
					else:
						cat.hide = False
					cat.save(update_fields=['desc','hide'])
					return redirect('/blog/{}'.format(cat.desc))
				except:
					return HttpResponse('<p>Error 1\n{}</p>'.format(form.errors.as_text))
				else:
					return HttpResponse('Unknown Cat Error')
		else:
			return HttpResponse('<p>Error 2\n{}</p>'.format(form.errors.as_text))

	template = loader.get_template('blog_admin.html')
	cats = Category.getCategories(hidden=1)
	posts = Post.objects.order_by('post_id')

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
	cats = Category.getCategories(hidden=0)
	post = Post.objects.get(post_id=int(Post.getPosts().count()))
	loginForm = LoginForm()

	if request.method == 'POST':
	    form = LoginForm(request.POST or None)
	    if form.is_valid():
	        uservalue = form.cleaned_data.get("username")
	        passwordvalue = form.cleaned_data.get("password")

	        user = authenticate(username=uservalue, password=passwordvalue)

	        if user is not None: #The user is valid
	            login(request, user)
	            return redirect('blogAdmin')
	        else: #The user is invalid
	            context= {
					'cats': cats,
					'post': post,
					'form': form,
					'error': 'The username and password combination is incorrect'
					}
	            return HttpResponse(template.render(context, request))
	    else: #The form is invalid
	        context= {
				'form': form
				}
	        return HttpResponse(template.render(context, request))
	else:

		context = {
			'cats': cats,
			'post': post,
			'form': loginForm,
		}

		return HttpResponse(template.render(context, request))

	return HttpResponse('Unknown Blog Error')

def blogLogout(request):
	logout(request)
	return HttpResponse('Blog Logout Page')
