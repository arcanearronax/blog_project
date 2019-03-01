from django.db import models

class Category(models.Model):
	id = models.IntegerField(primary_key=True)
	desc = models.CharField(max_length=20)
	hide = models.BooleanField(default=False)

	def __str__(self):
		return self.desc

	def getCategories(hidden=0):
		if (hidden):
			return Category.objects.order_by('id')
		return Category.objects.filter(hide=0).order_by('id')



class Post(models.Model):
	id = models.IntegerField(primary_key=True)
	cat = models.ForeignKey(Category, on_delete=models.CASCADE, default=0)
	title = models.CharField(max_length=100)
	text = models.CharField(max_length=4000)
	pub_date = models.DateTimeField(auto_now_add=True, blank=True)

	def __str__(self):
		return self.title

<<<<<<< HEAD
	def getPosts(hidden=0, order='id', reverse=0):
		assert order in ('id', 'pub_date')
		if (reverse):
			order = '-{}'.format(order)
		if (hidden):
			return Post.objects.order_by(order)
		#return Post.objects.filter(hide=0).order_by(order)
		return Post.objects.exclude(desc=Category.objects.filter(hide=0).values_list('desc',flat=True))
=======
	# Need to fix this up a bit and make it a bit easier to use
	def getPosts(hidden=0, order='id', reverse=0, num=-1, cat=-1, id=-1):
		assert order in ('id', 'pub_date')

		if (id > -1):
			return Post.objects.filter(id=id)

		if (reverse):
			order = '-{}'.format(order)

		if (hidden):
			posts = Post.objects.filter(cat=Category.objects.filter(hide=hidden))
		else:
			posts = Post.objects

		if (cat != -1):
			posts = posts.filter(cat=cat)

		return posts
>>>>>>> Updated the templates being used to be less clunky and rearranged a fair bit of the code. Need to work on purging stuff that isnt being used and then fix up the admin page and login functionality.
