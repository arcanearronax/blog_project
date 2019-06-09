from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.shortcuts import redirect
from .models import Post, Category
from .forms import PostForm, CatForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.views import View
import logging

logger = logging.getLogger(__name__)

class BlogView(View):
    logger.info('Initiate: BlogView')

    user = User()

    # Class variables, so we don't repeatedly hit the database
    _cat = Category
    _post = Post
    _post_form = PostForm
    _cat_form = CatForm

    @classmethod
    def set_cat_query(cls,*args):
        logger.debug('set_cat_query: {}'.format(args))
        if (args):
            cls._cat_query = args[0]
        else:
            cls._cat_query = cls._cat.get_objects

    @classmethod
    def get_cat_query(cls,**kwargs):
        try:
            return cls._cat_query(**kwargs)
        except Exception as e:
            logger.debug('Blog View: Updating cat_query')
            logger.error('Exception: {}'.format(e))
            cls.set_cat_query(cls._cat.get_objects)
        return cls._cat_query(**kwargs)

    @classmethod
    def set_post_query(cls,*args):
        logger.debug('set_post_query: {}'.format(args))
        if (args):
            cls._post_query = args[0]
        else:
            cls._post_query = cls._post.get_query

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
    def set_cat_obj(cls,*args):
        logger.debug('set_cat_obj: {}'.format(args))
        if (args):
            cls._cat_obj = args[0]
        else:
            cls._cat_obj = cls._cat.objects.get

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
            cls.set_cat_obj()
        return cls.get_cat_obj(**kwargs)

    @classmethod
    def set_post_obj(cls,*args):
        logger.debug('set_post_obj: {}'.format(args))
        if (args):
            cls._post_obj = args[0]
        else:
            cls._post_obj = cls._post.objects.get

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
            cls.set_post_obj()
        return cls.get_post_obj(**kwargs)

    @classmethod
    def get_post_form(cls,**kwargs):
        logger.debug('Get post form')
        try:
            return cls._post_form(**kwargs)
        except Exception as e:
            logger.error('get_post_form-error: {}').format(e)
            raise Exception('Form Exception: {}'.format(e))
        return None

    @classmethod
    def get_cat_form(cls,**kwargs):
        logger.debug('Get cat form')
        try:
            return cls._cat_form(**kwargs)
        except Exception as e:
            logger.error('get_cat_form-error: {}'.format(e))
            raise Exception('Form Exception: {}'.format(e))

    # Need to figure out why this isn't redirecting
    @login_required(login_url='/login/')
    def blogAdmin(self,request,error):
        logger.info('Enter: blogAdmin')
        logger.debug('---USER: {}'.format(request.user))

        try:
            cats = BlogView.get_cat_query(order='cat_id')
            posts = BlogView.get_post_query(order='post_id')
        except Exception as error:
            logger.error('blogAdmin-error: {}'.format(error))
            template,context,error = self.blogError(request)
        else:
            template = loader.get_template('blog_admin.html')
            context = {
                'cats': cats,
                'posts': posts,
                'pcnt': posts.count(),
                'ccnt': cats.count(),
                'post_json': Post.get_json(),
                'cat_json': Category.get_json(),
                'pForm': BlogView.get_post_form(),
                'cForm': BlogView.get_cat_form(),
                'username': request.user.first_name,
            }

        #return HttpResponse(template.render(context, request))
        return template,context,error

    # Use this as a quick way to catch errors
    def blogError(self,request,error):
        logger.info('Enter Blog Error')
        logger.error('  --{}'.format(error))
        template = loader.get_template('blog_error.html')
        context = {
            'error': error
        }
        return template,context,error

    # This is responsible for handling any get requests
    def get(self,request,desc=None,pk=None):
        logger.info('Enter Get: {} - {}'.format(desc,pk))
        logger.debug('path_info: {}'.format(request.path_info))

        # Use this is a temp solution
        template = None
        context = None
        error = None

        # This is being used as a temp solution to process non-category requests
        if request.path_info == '/admin/':
            logger.info('Requested Admin Page')
            try:
                logger.debug('Get-Admin')
                template,context,error = self.blogAdmin(request,error)
            except Exception as error:
                logger.debug('Cannot enter admin: {}'.format(error))
                template,context,error = self.blogError(request,error)

        # If we don't have desc, display the homepage
        elif desc is None:
            logger.debug('Return Homepage')
            template = loader.get_template('blog_home.html')
            context = {
                'cats': BlogView.get_cat_query(hide=0,order='cat_id')
            }

        # If we don't have pk, display the category page
        elif pk is None:
            logger.debug('Return Category Page')
            try:
                logger.debug('Test1')
                if request.user.is_authenticated:
                    cat = BlogView.get_cat_obj(desc=desc)
                else:
                    cat = BlogView.get_cat_obj(desc=desc,hide=0)
                logger.debug('test2: {}'.format(cat.__class__))
                posts = BlogView.get_post_query(cat_id=cat.cat_id,order='-post_id')
                post = BlogView.get_post_query(cat_id=cat.cat_id).last()
            except Exception as error:
                #error = e
                logger.error('Caught in GET: {}'.format(error))
                template,context,error = self.blogError(request,error)
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
                template,context,error = self.blogError(request,error)

            if post.cat_id != cat.cat_id:
                error = 'Category/post mismatch specified: {} - {}'.format(desc,pk)
                # Need to figure out a proper way to redirect
                template,context,error = self.blogError(request,error)
            else:
                template = loader.get_template('blog_post.html')
                context = {
                    'post': post,
                    'cat': cat,
                }

        # Building a new means to render pages
        logger.debug('Returning - GET')
        return HttpResponse(template.render(context, request))


    # Process POST requests - admin page
    def post(self,request):
        logger.info('Enter: POST')
        logger.debug('path_info: {}'.format(request.path_info))

        ### Begin functions ###

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
                    logger.error('Failed Post Update')
                    return None
                else:
                    logger.error('Unkown Post Error')
                    return None

        def processCategory(form,request):
            logger.debug('Enter: processCategory')

            error = None

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

        logger.info('Enter Admin')
        logger.debug('-- {}'.format(request.POST.__dict__))

        if 'PostReq' in request.POST:
            logger.info('Received PostReq request')

            # Get the post form and process it
            form = PostForm(request.POST)
            post = processPost(form,request)
            logger.debug('processPost - {}'.format(post))

            # Post saved successfully
            if post:
                try:
                    logger.debug('Returning Post')
                except Exception as e:
                    template = loader.get_template('blog_admin.html')
                    context = {
                        'cats': BlogView.get_cat_query(),
                        'posts': BlogView.get_post_query(),
                        'pcnt': posts.count(),
                        'ccnt': cats.count(),
                        'post_json': Post.get_json(),
                        'cat_json': Category.get_json(),
                        'pForm': BlogView.get_post_form(),
                        'cForm': BlogView.get_cat_form(),
                        'username': request.user.first_name,
                        'error': 'Please fill out all fields',
                    }
                else:
                    return redirect('/{}/{}/'.format(Post.get_cat_desc(post.post_id),post.post_id))

            # Post failed
            template = loader.get_template('blog_admin.html')
            context = {
                'cats': BlogView.get_cat_query(),
                'posts': BlogView.get_post_query(),
                'post_json': Post.get_json(),
                'cat_json': Category.get_json(),
                'pForm': BlogView.get_post_form(),
                'cForm': BlogView.get_cat_form(),
                'username': request.user.first_name,
                'error': 'Failed to submit post',
            }

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
            template = loader.get_template('blog_admin.html')
            context = {
                'cats': cats,
                'posts': posts,
                'pcnt': posts.count(),
                'ccnt': cats.count(),
                'post_json': Post.get_json(),
                'cat_json': Category.get_json(),
                'pForm': BlogView.get_post_form(),
                'cForm': BlogView.get_cat_form(),
                'username': request.user.first_name,
                'error': 'Failed to submit category'
            }

        # Return the page if we had error
        return HttpResponse(template.render(context, request))
