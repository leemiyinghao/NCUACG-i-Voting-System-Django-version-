from django.contrib import admin
from .models import VoteList, VoteableUser, FetchVote, VoteTicket, Options
# Register your models here.

class EditOptions(admin.TabularInline):
    model = Options
    extra = 3
@admin.register(VoteList)
class ManageVoteList(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title', 'describe', 'voteType']}),
        ('date_option', {'fields': ['pubDate', 'expireDate']}),
        ('select_vote_config', {'fields': ['maxSelectCount']}),
        ('video_vote_config', {'fields': ['videoURL','videoLength']}),
    ]
    inlines = [EditOptions]
    list_display = ('id', 'title', 'voteType', 'pubDate', 'expireDate')
    readonly_fields = ('pubDate', )
@admin.register(VoteableUser)
class ManageVoteableUser(admin.ModelAdmin):
    list_display = ('id', 'userName', 'nickName')
@admin.register(FetchVote)
class ViewFetchVote(admin.ModelAdmin):
    list_display = ('userName', 'roomID', 'fetchDate')
    readonly_fields = ('userName', 'roomID', 'fetchDate')
@admin.register(VoteTicket)
class ViewVoteTicket(admin.ModelAdmin):
    list_display = ('roomID', 'roomVoteType', 'option_or_score', 'userName', 'doneVideo')
    readonly_fields = ('roomID', 'roomVoteType', 'option_or_score', 'userName', 'doneVideo')
