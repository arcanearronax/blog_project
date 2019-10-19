from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.shortcuts import redirect
#from .models import Post, Category
#from .forms import PostForm, CatForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.views import View



# Create your views here.

class RestView(View):
	def get(self,request):
		return HttpResponse('Success')
