from django.db import models

class VoteableUser(models.Model):
    userName = models.CharField(max_length=50)
    nickName = models.CharField(max_length=50)
    icon = models.ImageField(upload_to = 'user_icon', default = 'user_icon/Default.png')
    
class VoteList(models.Model):
    title = models.CharField(max_length=50)
    describe = models.TextField(max_length=500)
    VOTE_TYPE = (
        ("v", "videoVote"),
        ("s", "select"),
    )
    voteType = models.CharField(max_length=1, choices=VOTE_TYPE)
    pubDate = models.DateTimeField('date published')
    expireDate = models.DateTimeField('date expire')
    videoURL = models.URLField()
    maxSelectCount = models.IntegerField(default=1)
    videoLength = models.IntegerField(default=0)
    
class FetchVote(models.Model):
    userName = models.CharField(max_length=50)
    roomID = models.ForeignKey(VoteList)
    fetchDate = models.DateTimeField()

class Options(models.Model):
    roomID = models.ForeignKey(VoteList)
    text = models.TextField(max_length=500)

class VoteTicket(models.Model):
    roomID = models.ForeignKey(VoteList)
    userName = models.CharField(max_length=50)
    score = models.IntegerField(default=0)
    optionID = models.ForeignKey(Options)
    doneVideo = models.BooleanField(default=False)  
