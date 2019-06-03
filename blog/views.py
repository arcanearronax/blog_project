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

	# Displays a single blog post
	def blogPost(self,request,desc,pk):
		logger.info('Enter: blogPost')

		# Get the category
		cat = Category.objects.get(desc=desc)
		logger.debug('cat: {}'.format(cat))

		# Get the post
		post = Post.objects.get(pk=pk)
		logger.debug('post: {}'.format(post))

		# Make sure the post exists under the category
		assert post.cat_id == cat.cat_id, 'Incorrect category specified: {} - {}'.format(desc,pk)

		# Render the page
		template = loader.get_template('blog_post.html')
		context = {
			'post': post,
			'cat': cat,
		}
		return HttpResponse(template.render(context, request))

	# Displays the blog category page
	def categoryHome(self,request, desc):
		logger.info('Enter: categoryHome')

		# Get the category or bail out
		try:
			cat = Category.objects.get(desc=desc)
		# In case multiple categories with the same name are found
		except Category.MultipleObjectsReturned as mor:
			logger.error('Multiple Categories Found: {}'.format(desc))
			return HttpResponse('Too Many Categories', status=500)
		# In case the category does not exist.
		except Category.DoesNotExist as dne:
			logger.error('Category Does not Exist: {}'.format(desc))
			return HttpResponse('Category Does not Exist: {}'.format(desc),status=404)
		# Whatever other exception could occur
		except Exception as e:
			logger.error('Unknown Error - {}'.format(e.__class__))
			return HttpResponse('Unknown Error', status=500)

		# Get the posts
		try:
			posts = Post.get_objects(cat_id=cat.cat_id,order='-post_id')
			logger.debug('posts = {}'.format(posts))
			post = posts[0]
		except Exception as e:
			logger.error('posts[0]: {}'.format(e))
			return self.blogHome(request)

		# Finalize our info
		template = loader.get_template('blog_category.html')
		context = {
			'posts': posts,
			'cat': cat,
			'post': post,
		}

		return HttpResponse(template.render(context, request))

	# Display the blog homepage
	def blogHome(self,request):
		logger.info('Enter: blogHome')

		# Get the categories
		cats = Category.getCategories()
		logger.debug('catCount: {}'.format(cats.count()))

		# Get a post to display
		post = Post.objects.get(post_id=int(Post.getPosts().count()))
		logger.debug('post: {}'.format(post))

		# Render the page
		template = loader.get_template('blog_home.html')
		context = {
			'cats': cats,
			'post': post,
		}
		return HttpResponse(template.render(context, request))

	# Use this to render login page
	def blogLogin(self,request):
		logger.info('Enter: blogLogin-UPDATED')

		# Get Categories
		cats = Category.getCategories(hidden=0)
		logger.debug('catCount: {}'.format(cats.count()))

		# Get post
		post = Post.objects.get(post_id=int(Post.getPosts().count()))
		logger.debug('post: {}'.format(post))

		# Get login form
		loginForm = LoginForm()

		# Render the page
		template = loader.get_template('blog_login.html')
		context = {
			'cats': cats,
			'post': post,
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

		template = loader.get_template('blog_admin.html')
		cats = Category.objects.all().order_by('cat_id')
		posts = Post.objects.order_by('post_id')

		pForm = PostForm()
		pForm.id = -1
		cForm = CatForm()
		cForm.id = -1

		try:
			logger.info('postCount: {}'.format(posts.count()))
			logger.info('catCount: {}'.format(cats.count()))
		except:
			logger.info('Failed to log info')

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

		# If don't have desc, display the homepage
		if desc is None:
			return self.blogHome(request)

		# If we don't have pk, display the category page
		elif pk is None:
			# We Return the category page or 404
			try:
				return self.categoryHome(request,desc)
			# Whatever failure could occur
			except Exception as e:
				logger.error('No Category: {}'.format(e))
				return HttpResponse('No Category: {}'.format(desc),status=404)

		# We have desc and pk, so display the the blogpage
		else:
			# We return the post page or 404
			try:
				return self.blogPost(request,desc,pk)
			# In case the pk doesn't exist under the category
			except AssertionError as a:
				logger.error('Cat post mismatch - {}'.format(a))
				return HttpResponse('Category-Post conflict: {} - {}'.format(desc,pk), status=406)
			# In case the category doesn't exist
			except Category.DoesNotExist as dne:
				logger.error('Category Does not Exist: {}'.format(desc))
				return HttpResponse('Category Does not Exist: {}'.format(desc))
			# Whatever other failure could occur
			except Exception as e:
				logger.error('Unknown Failure - {}'.format(e))
				return HttpResponse('Unknown Failure: {} - {}'.format(desc,pk))

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



def blogError(request):
	return HttpResponse('You got an error.')

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
