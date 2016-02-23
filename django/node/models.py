from django.db import models
import uuid, os
from django.conf import settings
from mptt.models import MPTTModel, TreeForeignKey

import logging
logger = logging.getLogger(__name__)

class Category(MPTTModel):
    name = models.CharField(max_length=150, unique=True)
    weight = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    slug = models.SlugField(max_length=150, unique=True)
    
    class MPTTMeta:
        order_insertion_by = ['weight']
        
    def save(self, *args, **kwargs):
        """
        Create a album folder in settings.UPLOAD_ROOT, before save 
        a new album into database.
        """
        logger.debug('album model save {0}'.format(__name__))
        
        category_directory = os.path.join(settings.MEDIA_ROOT, self.slug)
        if not os.path.exists(category_directory):
            os.makedirs(category_directory)
     
        super(Category, self).save(*args, **kwargs)
        
    def __unicode__(self):
        return self.name

from storage import OverwriteStorage

def file_upload_path(instance, filename):
    ''' 
    build file upload path
    e.g.
    upload_path = album_name/f47ac10b-58cc-4372-a567-0e02b2c3d479.jpg
    '''
    file_extension = filename.split('.')[-1]
    saved_name = "{}.{}".format(instance.id, file_extension)
    return os.path.join(instance.category.slug, saved_name)

class UploadFile(models.Model):
    """A page object contains multiple text blocks"""
    id = models.CharField(max_length=64, primary_key=True, verbose_name=u"UUID key",
                 default=uuid.uuid4)
    
    name = models.CharField(max_length=150)
    category = models.ForeignKey('Category', null=True)
    created = models.DateTimeField(db_index=True, auto_now_add=True)
    upload_file = models.FileField(storage=OverwriteStorage(), upload_to=file_upload_path)
    active = models.BooleanField(default=True)
    
    def __unicode__(self):
        return self.name
    
    
# Receive the pre_delete signal and delete the file associated with the model instance.
from django.db.models.signals import pre_delete, pre_save, post_delete
from django.dispatch.dispatcher import receiver

import shutil
@receiver(post_delete, sender=Category)
def auto_delete_category_on_delete(sender, instance, **kwargs):
    """Deletes file from filesystem
    when corresponding Category object is deleted.
    """
    category_directory = os.path.join(settings.MEDIA_ROOT, instance.slug)
    if os.path.exists(category_directory):
        logger.debug('category on delete trigger delete catagory {0}'.format(category_directory))
        shutil.rmtree(category_directory)
    
# note: do not change category name and parent unless necessary
# @receiver(pre_save, sender=Category)
# def auto_move_category_on_change(sender, instance, **kwargs):
#     """Move sub directory from filesystem
#     when corresponding File object is changed.
#     """
#     logger.debug('triggered off by change category {0}'.format(instance))
#     if not instance.id:
#         return False
#  
#     try:
#         old_category = Category.objects.get(pk=instance.id)
#     except UploadFile.DoesNotExist:
#         return False
#  
#     # get old_parent and past parent
#     # build source and dest path
#     # update path via os.rename(s, d)
#  
#     new_file = instance.upload_file
#     
#     # if parent is different, move the new category under new parent
#     
#     # if parent is same and slug updated, rename the folder name
#     if not old_file == new_file:
#         old_file.delete(False)
        
@receiver(pre_delete, sender=UploadFile)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """Deletes file from filesystem
    when corresponding Image object is deleted.
    """
    # Pass false so FileField doesn't save the model.
    instance.upload_file.delete(False)

@receiver(pre_save, sender=UploadFile)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """Update file from filesystem
    when corresponding File object is changed.
    """
    logger.debug('triggered off by delete file {0}'.format(instance.upload_file))
    if not instance.id:
        return False
 
    try:
        old_file = UploadFile.objects.get(pk=instance.id).upload_file
    except UploadFile.DoesNotExist:
        return False
 
    new_file = instance.upload_file
    if not old_file == new_file:
        old_file.delete(False)