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

class Category(models.Model):
	cat_id = models.IntegerField(primary_key=True)
	desc = models.CharField(max_length=20)
	hide = models.NullBooleanField(default=False)
	change_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

	def __str__(self):
		return self.desc

	def get_json():
		return dict(
			descs=[cat.desc for cat in Category.objects.filter(hide=1).order_by('cat_id')],
			hides=[cat.hide for cat in Category.objects.filter(hide=1).order_by('cat_id')]
		)

class Post(models.Model):
	post_id = models.IntegerField(primary_key=True)
	cat = models.ForeignKey(Category, on_delete=models.CASCADE)
	title = models.CharField(max_length=100)
	text = models.CharField(max_length=4000)
	pub_date = models.DateTimeField(auto_now_add=True)
	change_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

	def __str__(self):
		return self.title

	# This is being used for the javascript code. This will likely need to
	# be updated to call the API.
	def get_json():
		json = dict(
			titles=[post.title for post in Post.objects.order_by('post_id')],
			texts=[post.text for post in Post.objects.order_by('post_id')],
			cats=[post.cat.cat_id for post in Post.objects.order_by('post_id')]
		)
		return json
