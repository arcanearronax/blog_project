from django.db import models
from django.utils.timezone import now
import logging

icon_choices = (
	('calculator', 'fa-calculator'),
	('atom', 'fa-atom'),
	('computer', 'fa-desktop'),
	('cat', 'fa-cat'),
	('default', 'fa-blog'),
)

logger = logging.getLogger('blog.views')

# Just using this for a temporary fix
class AuxModel():

	@classmethod
	def count_objects(cls,**kwargs):
		logger.debug('--Count Objects: {}'.format(cls.__name__))
		# filter = 'cls.objects'
		# for k,v in kwargs.items():
		# 	filter += '.filter({}=\'{}\')'.format(k,v)
		# logger.debug('filter: {}'.format(filter))
		# return eval(filter).count()
		return cls.get_objects(kwargs).count()

	@classmethod
	def get_objects(cls,order=None,**kwargs):
		logger.debug('--Get Objects: {}'.format(cls.__name__))
		filter = 'cls.objects'

		if kwargs:
			for k,v in kwargs.items():
				logger.debug('filt--{}: {}'.format(k,v))
				filter += '.filter({}=\'{}\')'.format(k,v)
		else:
			filter += '.all()'
		if order:
			filter += '.order_by(\'{}\')'.format(order)

		logger.debug('filter: {}'.format(filter))
		tmp = eval(filter)
		return tmp

	@classmethod
	def next_pk(cls):
		return eval('{}.{}'.format('cls.objects.order_by(\'pk\').last()',cls._meta.pk.name)) + 1

class Category(models.Model, AuxModel):
	cat_id = models.IntegerField(primary_key=True)
	desc = models.CharField(max_length=20)
	hide = models.NullBooleanField(default=False)
	change_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

	def __str__(self):
		return self.desc

	def getCategories(hidden=0, cat_id=0):
		if (cat_id > 0):
			return Category.objects.filter(cat_id=cat_id)[0]

		cats = Category.objects
		if (hidden):
			cats = cats.order_by('cat_id')
		else:
			cats = cats.filter(hide=0).order_by('cat_id')
		return cats

	def get_json():
		return dict(
			descs=[cat.desc for cat in Category.getCategories(hidden=1).order_by('cat_id')],
			hides=[cat.hide for cat in Category.getCategories(hidden=1).order_by('cat_id')]
		)

	@classmethod
	def get_pk_by_desc(cls,desc):
		tmp = cls.objects.get(desc=desc).cat_id
		logger.debug('pk_by_desc: {}'.format(tmp))
		return cls.objects.get(desc=desc).cat_id

class Post(models.Model,AuxModel):
	post_id = models.IntegerField(primary_key=True)
	cat = models.ForeignKey(Category, on_delete=models.CASCADE, default=0, db_column='cat_id')
	title = models.CharField(max_length=100)
	text = models.CharField(max_length=4000)
	pub_date = models.DateTimeField(blank=True, default=now)
	change_date = models.DateTimeField(blank=True, null=True,default=now)

	def __str__(self):
		return self.title

	# Need to fix this up a bit and make it a bit easier to use
	def getPosts(hidden=0, order='post_id', reverse=0, num=-1, cat_id=-1, post_id=-1):
		assert order in ('post_id', 'pub_date')

		if (post_id > -1):
			return Post.objects.filter(post_id=post_id)[0]

		if (reverse):
			order = '-{}'.format(order)

		if (hidden):
			posts = Post.objects.all()
		else:
			posts = Post.objects.filter(cat=1)

		if (cat_id != -1):
			posts = posts.filter(cat=cat_id)

		return posts

	def get_json():
		json = dict(
			titles=[post.title for post in Post.objects.order_by('post_id')],
			texts=[post.text for post in Post.objects.order_by('post_id')],
			cats=[post.cat.cat_id for post in Post.objects.order_by('post_id')]
		)
		return json

	@classmethod
	def get_cat_desc(cls,pk):
		return cls.objects.get(pk=pk).cat.desc
