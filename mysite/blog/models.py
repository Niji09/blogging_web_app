from django.db import models
from django.urls import reverse
from django.utils import timezone
# Create your models here.

class Post(models.Model):
	auther = models.ForeignKey('auth.User', on_delete=models.CASCADE)
	title = models.CharField(max_length=256)
	text = models.TextField()
	create_date = models.DateTimeField(default=timezone.now)
	published_date = models.DateTimeField(blank=True, null=True)

	def publish(self):
		self.published_date = timezone.now()
		self.save()

	def approve_comments(self):
		return self.comment
	def get_absolute_url(self):
		return reverse("blog:post_detail",kwargs={'pk':self.pk})

	def __str__(self):
		return self.title


class Comment(models.Model):
	post = models.ForeignKey('Post', related_name='comment', on_delete=models.CASCADE)
	viewer = models.ForeignKey('auth.User', on_delete=models.CASCADE)
	text = models.TextField()
	create_date = models.DateTimeField(default=timezone.now)
	approve_comment= models.BooleanField(default=False)

	def approve(self):
		self.approve_comment = True
		self.save()

	def get_absolute_url(self):
		return reverse("blog:post_detail", kwargs={'pk':self.pk})

	def __str__(self):
		return self.text


