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

	# Need to fix this up a bit and make it a bit easier to use
	def getPosts(hidden=0, order='id', reverse=0, num=-1, cat=-1, id=-1):
		assert order in ('id', 'pub_date')

		if (id > -1):
			return Post.objects.filter(id=id)

		if (reverse):
			order = '-{}'.format(order)

		if (hidden):
			posts = Post.objects.all()
		else:
			posts = Post.objects.filter(cat__in=Category.objects.filter(hide=0))

		if (cat != -1):
			posts = posts.filter(cat=cat)

		return posts
