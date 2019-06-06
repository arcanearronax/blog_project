from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from .forms import LoginForm
from django.template import loader
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
import logging


logger = logging.getLogger('blog.views')

class BlogLogin(LoginView):
    logger.info('Initializing: BlogLogin')

    template_name = 'blog_login.html'
    redirect_field_name = '/login/'
    next = '/login/'
    #authentication_form
    #extra_context
    #redirect_authenticated_user

    def get(self,request):
        logger.info('Enter: blogLogin - GET')

        # Get login form
        loginForm = LoginForm()

        # Render the page
        template = loader.get_template(self.template_name)
        context = {
            'form': loginForm,
        }
        return HttpResponse(template.render(context, request))
        #return template,context,error

    def post(self,request):
        logger.info('Enter: blogLogin - POST')

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
                    login(request,user)
                    logger.info('User authenticated: {}'.format(user))
                    return user

            else:
                logger.error('login-form-error: {}'.format(form.errors))

            # Something wasn't right
            return None

        # Create our form object
        logger.debug('Calling login form')
        try:
            form = LoginForm(request.POST)
        except Exception as e:
            logger.error('login-error - {}'.format(e))
        else:
            user = processUser(form,request)
            logger.debug('login successful: {}'.format(user))
            return redirect('blogAdmin')

        # Authentication failed
        return HttpResponse('Failed to authenticate')

class BlogLogout(LogoutView):
    logger.info('Initializing: BlogLogout')

    next_page = '/'
    template_name = 'blog_logout.html'
    redirect_field_name = 'blogLogout'

    def get(self,request):
        logger.info('Enter Blog Logout-CLASS')
        try:
            logout(request)
        except Exception as error:
            logger.error('Logout-error: {}'.format(error))

        # Render the logout page
        template = loader.get_template(self.template_name)
        context = {

        }
        return HttpResponse(template.render(context, request))
