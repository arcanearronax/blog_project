from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.shortcuts import redirect
from .models import Post, Category
from .forms import PostForm, CatForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.views import View
import logging

logger = logging.getLogger(__name__)

class BlogView(View):
	logger.info('Initiate: BlogView')

	# Class variables, so we don't repeatedly hit the database
	_cat = Category
	_post = Post
	_cat_query = None
	_post_query = None
	_cat_obj = None
	_post_obj = None

	@classmethod
	def get_cat_query(cls,**kwargs):
		try:
			return cls._cat_query(**kwargs)
		except Exception as e:
			logger.debug('Blog View: Updating cat_query')
			logger.error('Exception: {}'.format(e))
			cls._cat_query = cls._cat.get_objects
			return cls._cat_query(**kwargs)

	@classmethod
	def get_post_query(cls,**kwargs):
		try:
			return cls._post_query(**kwargs)
		except Exception as e:
			logger.debug('Blog View: Updating post_query')
			logger.error('Exception: {}'.format(e))
			cls._post_query = cls._post.get_objects
			return cls._post_query(**kwargs)

	@classmethod
	def get_cat_obj(cls,**kwargs):
		logger.debug('Get cat object()')
		try:
			return cls._cat_obj(**kwargs)
		except cls._cat.DoesNotExist as dne:
			logger.debug('get_cat_obj-dne: {}'.format(dne))
			raise dne
		except Exception as e:
			logger.debug('Blog View: Updating cat_obj')
			cls._cat_obj = cls._cat.objects.get
		return cls.get_cat_obj(**kwargs)

	@classmethod
	def get_post_obj(cls,**kwargs):
		logger.debug('Get post objects()')
		try:
			return cls._post_obj(**kwargs)
		except cls._post.DoesNotExist as dne:
			logger.debug('get_post_obj-dne: {}'.format(dne))
			raise Exception('Post not found: {}'.format(kwargs))
		except Exception as e:
			logger.debug('Blog View: Updating post_obj')
			cls._post_obj = cls._post.objects.get
		return cls.get_post_obj(**kwargs)

	# Use this to render login page
	def blogLogin(self,request):
		logger.info('Enter: blogLogin-UPDATED')

		# Get login form
		loginForm = LoginForm()

		# Render the page
		template = loader.get_template('blog_login.html')
		context = {
			'cats': BlogView.get_cat_query(hide=0),
			'post': BlogView.get_post_obj(post_id=BlogView._post.count_objects()),
			'form': loginForm,
		}
		return HttpResponse(template.render(context, request))

	# Use this to process user logout
	def blogLogout(self,request):
		logger.info('Enter Blog Logout-UPDATED')

		# Let django handle the logout
		logout(request)

		# Render the logout page
		template = loader.get_template('blog_logout.html')
		context = {

		}
		return HttpResponse(template.render(context, request))

	def blogAdmin(self,request):
		logger.info('Enter: blogAdmin')
		logger.debug('REQUEST: {}'.format(request.POST))


		cats = BlogView.get_cat_query(order='cat_id')
		posts = BlogView.get_post_query(order='post_id')

		pForm = PostForm()
		pForm.id = -1
		cForm = CatForm()
		cForm.id = -1

		template = loader.get_template('blog_admin.html')
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

	def blogError(self,request,error):
		logger.info('Enter Blog Error')
		logger.error('  --{}'.format(error))
		template = loader.get_template('blog_error.html')
		context = {
			'error': error
		}
		return HttpResponse(template.render(context, request))

	# This is responsible for handling any get requests
	def get(self,request,desc=None,pk=None):
		logger.info('Enter Get: {} - {}'.format(desc,pk))
		logger.debug('path_info: {}'.format(request.path_info))

		# This is being used as a temp solution to process non-category requests
		if request.path_info == '/login/':
			return self.blogLogin(request)
		if request.path_info == '/logout/':
			return self.blogLogout(request)
		if request.path_info == '/admin/':
			return self.blogAdmin(request)

		# Below here is where we generate the normal blog pages

		# Let's gather up commonly used vars


		# Auxilliary
		error = None

		# If we don't have desc, display the homepage
		if desc is None:
			logger.debug('Return Homepage')
			template = loader.get_template('blog_home.html')
			context = {
				'cats': BlogView.get_cat_query(hide=0,order='cat_id')
			}

		# If we don't have pk, display the category page
		elif pk is None:
			logger.debug('Return Category Page')
			try:
				cat = BlogView.get_cat_obj(desc=desc,hide=0)
				posts = BlogView.get_post_query(cat_id=cat.cat_id,order='-post_id')
				post = BlogView.get_post_query(cat_id=cat.cat_id).last()
			except Exception as error:
				#error = e
				logger.error('Caught in GET: {}'.format(error))
				return HttpResponse(error)
			else:
				template = loader.get_template('blog_category.html')
				context = {
					'posts': BlogView.get_post_query(cat_id=cat.cat_id,order='-post_id'),
					'cat': cat,
					'post': BlogView.get_post_query(cat_id=cat.cat_id).last(),
					'error': error,
				}

		# We have desc and pk, so display the the blogpage
		else:
			logger.debug('Return Post Page')
			try:
				cat = BlogView.get_cat_obj(desc=desc,hide=0)
				post = BlogView.get_post_obj(pk=pk)
			except Exception as error:
				logger.error('Caught Exception in GET: {}'.format(error))
				return self.blogError(request,error)
			assert post.cat_id == cat.cat_id, 'Incorrect category specified: {} - {}'.format(desc,pk)
			template = loader.get_template('blog_post.html')
			context = {
				'post': post,
				'cat': cat,

			}


		# Building a new means to render pages
		logger.debug('CONTEXT - {}'.format(context))
		return HttpResponse(template.render(context, request))


	# Process POST requests - admin page
	def post(self,request):
		logger.info('Enter: POST')
		logger.debug('path_info: {}'.format(request.path_info))

		### Begin functions ###

		# Let's trying creating a method here
		def processUser(form,request):
			logger.info('Enter: processUser')

			# Validate the form
			if form.is_valid():
				# Authenticate user credentials
				uservalue = form.cleaned_data.get("username")
				passwordvalue = form.cleaned_data.get("password")
				user = authenticate(username=uservalue, password=passwordvalue)

				# The user is valid
				if user is not None: #The user is valid
					login(request, user)
					logger.info('User authenticated: {}'.format(user))
					return user

			# Something wasn't right
			return None

		# Let's process a post form
		def processPost(form,request):
			logger.info('Enter: processPost')

			# validate the form, new posts go here
			if form.is_valid():
				logger.debug('Form is valid')

				# Initialize and update
				post = form.save(commit=False)
				post.post_id = Post.next_pk()
				post.title = request.POST.get('title')
				post.cat_id = request.POST.get('cat')
				post.text = request.POST.get('text')

				# Save the post object
				try:
					post.save()
				except Exception as e:
					logger.debug('post-save-failure: {}'.format(e))
				else:
					logger.info('New Post Saved: {}'.format(post.post_id))
					return post

				# some type of failure occurred
				return None

			# This indicates an edit should occur
			else:
				logger.debug('Post form is invalid')
				try:
					# Initialize and update the Post object
					post = Post.objects.get(post_id=int(request.POST.get('post_id'))+1)
					post.title = request.POST.get('title')
					post.cat = Category.getCategories(cat_id=int(request.POST.get('cat')))
					post.text = request.POST.get('text')

					# Save the post object
					try:
						post.save(update_fields=['title','cat_id','text'])
					except Exception as e:
						logger.error('post-update-fail: {}'.format(e))
					else:
						logger.info('Post Updated: {}'.format(post.post_id))
						return post

					# We failed somewhere
					return None

				except Exception as e:
					logger.error('Failed Post Update: {}'.format(post.post_id))
					return None
				else:
					logger.error('Unkown Post Error')
					return None

		def processCategory(form,request):
			logger.debug('Enter: processCategory')

			# validate the form, new posts go here
			if form.is_valid():
				logger.debug('Cat form is valid')

				# Initialize and update
				cat = form.save(commit=False)
				cat.cat_id = Category.objects.count() + 1
				cat.desc = request.POST.get('desc')
				if (request.POST.get('hide') == 'on'):
					cat.hide = True
				else:
					cat.hide = False

				# Save the category
				try:
					cat.save()
				except Exception as e:
					logger.error('cat-save-fail: {}'.format(e))
				else:
					logger.info('New Cat Saved: {}')
					return cat

				# We failed somewhere
				return None

			# we're updating a category
			else:
				logger.debug('Cat form is invalid')

				# Initialize and update the category
				logger.debug('GOT ID: {}'.format(request.POST.get('cat_id')))
				cat = Category.objects.get(cat_id=int(request.POST.get('cat_id'))+1)
				cat.desc = request.POST.get('desc')
				if (request.POST.get('hide') == 'on'):
					cat.hide = True
				else:
					cat.hide = False

				# Save the category
				try:
					cat.save(update_fields=['desc','hide'])
					logger.info('Cat Updated: {}'.format(cat.cat_id))
				except Exception as e:
					logger.error('cat-update-fail: {}'.format(e))
				else:
					return cat

		### End Functions ###

		# Is this for a login form?
		if request.path_info == '/login/':

			# Create our form object
			form = LoginForm(request.POST or None)
			logger.info('Received Login Request')

			# Authenticate the user
			if processUser(form,request):
				return redirect('blogAdmin')

			# Authentication failed
			return HttpResponse('Failed to authenticate')

		if request.path_info == '/admin/':
			logger.debug('Enter Admin')

			if 'PostReq' in request.POST:
				logger.info('Received PostReq request')

				# Get the post form and process it
				form = PostForm(request.POST)
				post = processPost(form,request)
				logger.debug('processPost - {}'.format(post.__dict__))

				# Post saved successfully
				if post:
					logger.debug('Returning Post')
					return redirect('/{}/{}/'.format(Post.get_cat_desc(post.post_id),post.post_id))

				# Post failed
				return HttpResponse('Failed Post')

			elif 'CatReq' in request.POST:
				logger.info('Received CatReq request')

				# Get the cat form and process it
				form = CatForm(request.POST)
				cat = processCategory(form,request)
				logger.debug('processCategory - {}'.format(cat.__dict__))

				# Cat saved successfully
				if cat:
					logger.debug('Returning Category')
					return redirect('/{}/'.format(cat.desc))

				# Cat failed
				return HttpResponse('Failed Category')


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
