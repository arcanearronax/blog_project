from django.db import models
import logging

logger = logging.getLogger(__name__)

icon_choices = (
	('calculator', 'fa-calculator'),
	('atom', 'fa-atom'),
	('computer', 'fa-desktop'),
	('cat', 'fa-cat'),
	('default', 'fa-blog'),
)

class NewCategory(models.Model):
	logger.debug('New Category Instantiated')
	cat_id = models.AutoField(primary_key=True)
	desc = models.CharField(max_length=20)
	hide = models.NullBooleanField(default=False)
	change_date = models.DateTimeField(auto_now_add=True,blank=True,null=True)

	def get(self,*args,**kwargs):
		logger.debug('Enter get')

		# We aren't doing anything with args, just kwargs
		if (args):
			logger.debug('\t--Got args, nothing to do.')

		# Loop over kwargs
		for k,v in kwargs.items():
			# Check if the kwarg is a model field
			if k in self.__dict__:
				logger.debug('Success: {}'.format(k))
				eval('self.{} = {}'.format(k,v))
			else:
				logger.debug('Not Found: {}'.format(k))

	def getCat(*args,**kwargs):
		for k,v in kwargs.items():
			logger.debug('k={}\tv={}'.format(k,v))

	def getCategories(hidden=0,cat_id=0):
		raise NotImplementedError('Not Implemented')

	def get_json():
		raise NotImplementedError('Not Implemented')

class Category(models.Model):
	cat_id = models.AutoField(primary_key=True)
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

class Post(models.Model):
	post_id = models.AutoField(primary_key=True)
	cat = models.ForeignKey(Category, on_delete=models.CASCADE, default=0, db_column='cat_id')
	title = models.CharField(max_length=100)
	text = models.CharField(max_length=4000)
	pub_date = models.DateTimeField(auto_now_add=True, blank=True)
	change_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

	def __str__(self):
		return self.title

	# Replace this with a .get command
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

	# This is being used for the javascript code. This will likely need to
	# be updated to call the API.
	def get_json():
		json = dict(
			titles=[post.title for post in Post.objects.order_by('post_id')],
			texts=[post.text for post in Post.objects.order_by('post_id')],
			cats=[post.cat.cat_id for post in Post.objects.order_by('post_id')]
		)
		return json
