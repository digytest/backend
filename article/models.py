from django.db import models
import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    image_url = models.ImageField(upload_to='images/') 
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Article(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    link = models.CharField(max_length=100)
    category_id = models.ForeignKey( 
        Category, on_delete=models.CASCADE, related_name='articles'
    )
    category_image_url = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# Signal to update category_image_url
@receiver(post_save, sender=Article)
def update_category_image_url(sender, instance, created, **kwargs):
    """ Update category_image_url only when the article is newly created or the category changes """
    if instance.category_id:
        category_image = instance.category_id.image_url
        if category_image and instance.category_image_url != category_image:
            Article.objects.filter(id=instance.id).update(category_image_url=category_image)