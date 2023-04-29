from django.db import models

# Create your models here.
class MiscData(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    parent_id = models.CharField(max_length=20, null=True, blank=True)
    props = models.JSONField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    
