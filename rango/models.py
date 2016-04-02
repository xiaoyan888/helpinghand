from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# Create your models here.
class Category (models.Model): # inheriented from models.Model
    name = models.CharField(max_length=128, unique=True)# pk
    #title = models.CharField(max_length=128)
    #url = models.URLField()
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField()

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if self.id is None:
            self.slug = slugify(self.name)

        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

class Page (models.Model):
    category = models.ForeignKey(Category) #model.field
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0) # database model staor number of views


    def __unicode__(self):
        return self.title

class UserProfile (models.Model):
    # This line is required. Links UserProfile to a User model instance. with default 5 attribute
    user = models.OneToOneField(User)
    # The additional two attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    #upload_to attribute. The value of this attribute is conjoined with the projects
    # MEDIA_ROOT setting to provide a path with which uploaded profile images will be stored.
    #stored in profile_images directory
    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username

