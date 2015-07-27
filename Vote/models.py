from django.db import models
from django.utils import timezone
from datetime import timedelta

class VoteableUser(models.Model):
    userName = models.CharField(max_length=50)
    nickName = models.CharField(max_length=50)
    icon = models.ImageField(upload_to = 'usericon', default = '/static/usericon/default.png')

    def __unicode__(self):
        return self.nickName

class VoteList(models.Model):
    title = models.CharField(max_length=50)
    describe = models.TextField(max_length=500)
    VOTE_TYPE = (
        ("v", "videoVote"),
        ("s", "selectVote"),
    )
    voteType = models.CharField(max_length=1, choices=VOTE_TYPE)
    pubDate = models.DateTimeField('date published', default = timezone.now())
    expireDate = models.DateTimeField('date expire', default = timezone.now() + timedelta(days = 3))
    videoURL = models.URLField(null=True)
    maxSelectCount = models.IntegerField(default=1)
    videoLength = models.IntegerField(default=0)
    def hasUserFetchVote(self, _userName):
        if self.fetchvote_set.filter(userName = _userName).count() > 0:
            return True
        else:
            return False
    def __unicode__(self):
        return self.title

class FetchVote(models.Model):
    userName = models.CharField(max_length=50)
    roomID = models.ForeignKey(VoteList)
    fetchDate = models.DateTimeField()
    def __unicode__(self):
        return self.userName

class Options(models.Model):
    roomID = models.ForeignKey(VoteList)
    text = models.CharField(max_length=500)
    def hasUserVoteThisOption(self, _userName):
        return True if self.voteticket_set.filter(mute=False, userName=_userName) else False
    def __unicode__(self):
        return self.text

class VoteTicket(models.Model):
    roomID = models.ForeignKey(VoteList)
    userName = models.CharField(max_length=50)
    score = models.IntegerField(default=0)
    optionID = models.ForeignKey(Options, null=True)
    doneVideo = models.BooleanField(default=False)
    mute = models.BooleanField(default=False)
    def __unicode__(self):
        return self.roomID.title
    def roomVoteType(self):
        return 'Video Vote' if self.roomID.voteType == 'v' else 'Select Vote'
    def option_or_score(self):
        return self.score if self.roomID.voteType == 'v' else self.optionID
