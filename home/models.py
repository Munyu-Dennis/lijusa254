from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image

class Contant(models.Model):
    Your_Name = models.CharField(max_length=255)
    Subject = models.CharField(max_length=255)
    message = models.TextField()


class Profile(models.Model):
    position = models.CharField(max_length=255, blank=True, default='Lijusa Member')
    facebook = models.CharField(max_length=100, blank=True, default='#')
    instagram = models.CharField(max_length=100, blank=True, default='#')
    twitter = models.CharField(max_length=100, blank=True, default='#')
    linkedin = models.CharField(max_length=100, blank=True, default='#')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    def __str__(self):
        return f'{self.user.username} Profile' #display on the admin site
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 and img.width > 300:
            output_size = (600, 600)
            img.thumbnail(output_size)
            img.save(self.image.path)

class Blog(models.Model):
    the_photo = models.ImageField(upload_to='blog_pics')
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)#set's the time the post was posted
    author = models.ForeignKey(User, on_delete=models.CASCADE)#ON DELETE meaning if a user is deleted so does the posts of the user
    def __str__(self):
        return self.title
    def get_pk(self):
        p_k = {"pk" : self.pk}
        return p_k
    def get_absolute_url(self):
        p_k = self.get_pk()
        return reverse('blog-single', kwargs=p_k)
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.the_photo.path)
        if img.height > 300 and img.width > 300:
            output_size = (1024, 764)
            img.thumbnail(output_size)
            img.save(self.the_photo.path)


class Comment(models.Model):
    code = models.IntegerField()
    message = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)#set's the time the post was posted
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.title
    

class Wiseword(models.Model):
    the_words = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)


