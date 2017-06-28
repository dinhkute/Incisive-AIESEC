# -*- coding: utf-8 -*-

# Create your models here

import datetime

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.validators import MinValueValidator, MaxValueValidator
from froala_editor.fields import FroalaField
from django.db.models import Sum


@python_2_unicode_compatible
class  Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        now = timezone.now()
        return now -datetime.timedelta(days=1)  <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently'

@python_2_unicode_compatible
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete = models.CASCADE)
    choicet_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choicet_text



'''User Profile Model'''
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    description = models.CharField(max_length=500, default='')
    city = models.CharField(max_length=50, default='')
    university = models.CharField(max_length=50, default='')
    facebook = models.URLField(default='')
    phone = models.IntegerField(default=0)
    image = models.ImageField(upload_to='profile_image', blank=True)

    def __str__(self):
        return self.user.username
def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])


post_save.connect(create_profile, sender=User)


'''Recruitment Compain'''

'''Local Committe Model'''

@python_2_unicode_compatible
class  LocalCommittee(models.Model):
    local_committee = models.CharField(max_length=200, default='HN')
    City = models.CharField(max_length=200, default='Hanoi')

    def __str__(self):
        return self.local_committee


@python_2_unicode_compatible
class  Recruitment(models.Model):
    local_committee = models.ForeignKey(LocalCommittee, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    pub_date = models.DateTimeField('date published')
    content = FroalaField()
    def __str__(self):
        return self.name

@python_2_unicode_compatible
class  RecruitmentForm(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    recruiment_id = models.ForeignKey(Recruitment, on_delete=models.CASCADE)
    student_name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    skill = models.CharField(max_length=200)
    university = models.CharField(max_length=200)
    year_program = models.IntegerField()

    def __str__(self):
        return self.student_name


@python_2_unicode_compatible
class Round(models.Model):
    round_num = models.IntegerField()
    round_name = models.CharField(max_length=200)

    def __str__(self):
        return self.round_name


@python_2_unicode_compatible
class  Questionnaire(models.Model):
    recruitment_form =  models.ForeignKey(RecruitmentForm, on_delete=models.CASCADE)
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    question_name = models.CharField(max_length=200)
    answer = models.CharField(max_length=200)

    def __str__(self):
        return self.question_name

@python_2_unicode_compatible
class Creatia(models.Model):
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    cretia_name = models.CharField(max_length=200)
    point = models.IntegerField(validators=[MinValueValidator(0),
                                       MaxValueValidator(100)])

    def __str__(self):
        return self.cretia_name

    #def get_queryset(self):
     #   return super(Creatia, self).filter(round=1).values('round').annotate(sum=Sum('point'))

"""For Project Management"""

'''Kind of Project'''
@python_2_unicode_compatible
class ProjectOfKind(models.Model):

    project_kind = models.CharField(max_length=200)

    def __str__(self):
        return self.project_purpose

'''Project Model'''
@python_2_unicode_compatible
class Project(models.Model):
    project_kind = models.ForeignKey(ProjectOfKind, on_delete=models.CASCADE)
    local_committee = models.ForeignKey(LocalCommittee, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=200)
    project_description = models.TextField(max_length=1000)

    def __str__(self):
        return self.project_name

'''SubProject Model'''
@python_2_unicode_compatible
class SubProject(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    subproject_name = models.CharField(max_length=200)
    subproject_description = models.TextField(max_length = 1000)
    create_date = models.DateTimeField('Created Date')
    closed_date = models.DateTimeField('Closed Date')

    def __str__(self):
        return self.subproject_name

'''Event for Project'''
class PublishedEvent(models.Model):
    project = models.ForeignKey(SubProject, on_delete= models.CASCADE)
    event_name = models.CharField(max_length = 200)
    event_description = FroalaField()
    create_date = models.DateTimeField('Created Date')
    pub_date = models.DateTimeField('Publised Date')
    closed_date = models.DateTimeField('Closed Date')

    def __str__(self):
        return self.event_name

"""Customer Register"""
class RegisterEvent(models.Model):
    event = models.ForeignKey(PublishedEvent, on_delete = models.CASCADE)
    customer_name = models.CharField(max_length=200)
    customer_phone = models.IntegerField()
    customer_email = models.EmailField(max_length=200)
    question = models.CharField(max_length=500)

    def __str__(self):
        return self.customer_name

"""Task and assignTask"""
class Task(models.Model):
    staff = models.ForeignKey(User,on_delete = models.CASCADE)
    project = models.ForeignKey(SubProject, on_delete=models.CASCADE)
    task_name = models.CharField(max_length = 200)
    requirement = models.TextField(max_length=1000)
    submit_file = models.FileField(upload_to='profile_image')
    commemt = models.TextField(max_length = 1000, blank=True)
    due_date = models.DateTimeField('Due Date')

    def __str__(self):
        return self.task_name


