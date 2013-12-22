from django.db import models
from django.contrib.auth.models import User

class Userdata(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=100, blank=True)
    def __unicode__(self):
        return u'%s' % (self.name)
