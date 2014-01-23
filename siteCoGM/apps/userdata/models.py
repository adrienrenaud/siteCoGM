from django.db import models
from django.contrib.auth.models import User
import os

class Userdata(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=100, blank=True)
    def __unicode__(self):
        return u'%s' % (self.name)




def get_path(instance, filename):
    return os.path.join('userdata', 'user_%s'%instance.userdata.user.id, filename)

class Textfile(models.Model):
    userdata = models.ForeignKey(Userdata, related_name='textfiles')
    filetype = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    legend = models.TextField(max_length=1000, null=True, blank=True)
    # file = models.FileField(upload_to="userdata", null=True, blank=True)
    file = models.FileField(upload_to=get_path, null=True, blank=True)

