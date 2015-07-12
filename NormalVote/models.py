from django.db import models

# Create your models here.
class Question(models.Model):

    question_title = models.CharField(max_length=50)
    question_describe = models.TextField(max_length=500)

    pub_date = models.DateTimeField('date published')
    expire_date = models.DateTimeField('date expire')

    def __unicode__(self):
        return self.question_title
class Choice(models.Model):
    question = models.ForeignKey(Question)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __unicode__(self):
        return self.choice_text
