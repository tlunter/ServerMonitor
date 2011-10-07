from django.db import models
from django.contrib.auth.models import User, UserManager

# Create your models here.
class Account(models.Model):
    company = models.CharField('Company',max_length=255)
    owner = models.ForeignKey(User)

    def __unicode__(self):
        return str(self.company)

class CustomUser(User):
    account = models.ForeignKey(Account,blank=True,null=True)
    objects = UserManager()

    def __unicode__(self):
        return str(self.username)

class Server(models.Model):
    name = models.CharField('Name',max_length=255)
    owner = models.ForeignKey(Account)
    level = models.IntegerField()

    def __unicode__(self):
        return str(self.name)

class Monitor(models.Model):
    name = models.CharField('Name',max_length=255)
    server = models.ForeignKey(Server)

    types = (
                (u'HTTP',u'HTTP'),
                (u'Adv',u'Advanced'),
            )
    type = models.CharField('Type',max_length=4,choices=types)

    statuses =  (
                    (u'On',u'Active'),
                    (u'Off',u'Inactive'),
                )
    status = models.CharField('Status',max_length=3,choices=statuses)
    frequency = models.IntegerField('Frequency')

    def __unicode__(self):
        return str(self.name)

class Search(models.Model):
    monitor = models.ForeignKey(Monitor)
    address = models.CharField('URL',max_length=255)
    
    types = (
                (u'Cont',u'Contains'),
                (u'Exct',u'Is Exactly'),
                (u'Strt',u'Starts With'),
                (u'Ends',u'Ends With'),
            )
    type = models.CharField('Type',max_length=4,choices=types)

    value = models.CharField('Value',max_length=255)

class Socket(models.Model):
    monitor = models.ForeignKey(Monitor)
    address = models.CharField('Address',max_length=255)
    port = models.IntegerField('Port Number',max_length=255)

class Message(models.Model):
    monitor = models.ForeignKey(Monitor)
    types = (
                (u'SMS',u'SMS'),
                (u'Call',u'Phone Call'),
                (u'Mail',u'Email'),
            )
    type = models.CharField('Type',max_length=4,choices=types)
    address = models.CharField('Address',max_length=255)
