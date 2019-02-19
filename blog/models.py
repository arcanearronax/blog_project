from django.db import models

class Category(models.Model):
	id = models.IntegerField(primary_key=True)
	desc = models.CharField(max_length=20)
	hide = models.BooleanField(default=False)

	def __str__(self):
		return self.desc



class Post(models.Model):
	id = models.IntegerField(primary_key=True)
	cat = models.ForeignKey(Category, on_delete=models.CASCADE, default=0)
	title = models.CharField(max_length=100)
	text = models.CharField(max_length=4000)
	pub_date = models.DateTimeField(auto_now_add=True, blank=True)

	def __str__(self):
		return self.title
