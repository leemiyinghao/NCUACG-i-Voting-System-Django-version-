from django.db import models
from django.utils import timezone
from datetime import timedelta

class VoteableUser(models.Model):
    verbose_name = 'voteable user'
    verbose_name_plural = 'voteable user list'
    userName = models.CharField(max_length=50, verbose_name='user name')
    nickName = models.CharField(max_length=50, verbose_name='nick name')
    icon = models.ImageField(upload_to = 'usericon', default = '/static/usericon/default.png', verbose_name='user icon')

    def __unicode__(self):
        return self.nickName

class VoteList(models.Model):
    title = models.CharField(max_length=50, verbose_name='vote title')
    describe = models.TextField(max_length=500, verbose_name='vote describe')
    VOTE_TYPE = (
        ("v", "videoVote"),
        ("s", "selectVote"),
    )
    voteType = models.CharField(max_length=1, choices=VOTE_TYPE, verbose_name='vote type')
    pubDate = models.DateTimeField(default = timezone.now(), verbose_name='publish date')
    expireDate = models.DateTimeField(default = timezone.now() + timedelta(days = 3), verbose_name='expire date')
    videoURL = models.URLField(null=True, verbose_name='video URL')
    maxSelectCount = models.IntegerField(default=1, verbose_name='max selection')
    videoLength = models.IntegerField(default=0, verbose_name='video length')
    def hasUserFetchVote(self, _userName):
        if self.fetchvote_set.filter(userName = _userName).count() > 0:
            return True
        else:
            return False
    def __unicode__(self):
        return self.title

class FetchVote(models.Model):
    userName = models.CharField(max_length=50, verbose_name='user name')
    roomID = models.ForeignKey(VoteList)
    fetchDate = models.DateTimeField(verbose_name='fetch datetime')
    def __unicode__(self):
        return self.userName

class Options(models.Model):
    roomID = models.ForeignKey(VoteList)
    text = models.CharField(max_length=500, verbose_name='option title')
    def hasUserVoteThisOption(self, _userName):
        return True if self.voteticket_set.filter(mute=False, userName=_userName) else False
    def __unicode__(self):
        return self.text

class VoteTicket(models.Model):
    roomID = models.ForeignKey(VoteList)
    userName = models.CharField(max_length=50, verbose_name='user name')
    score = models.IntegerField(default=0)
    optionID = models.ForeignKey(Options, null=True)
    doneVideo = models.BooleanField(default=False, verbose_name='has user done the video?')
    mute = models.BooleanField(default=False, verbose_name='mute')
    def __unicode__(self):
        return self.roomID.title
    def roomVoteType(self):
        return 'Video Vote' if self.roomID.voteType == 'v' else 'Select Vote'
    def option_or_score(self):
        return self.score if self.roomID.voteType == 'v' else self.optionID
