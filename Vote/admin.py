from django.contrib import admin
from .models import VoteList, VoteableUser, FetchVote, VoteTicket, Options
from .views import invoiceList
# Register your models here.

class EditOptions(admin.TabularInline):
    model = Options
    extra = 3
@admin.register(VoteList)
class ManageVoteList(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title', 'hashSetKey', 'describe', 'voteType']}),
        ('date_option', {'fields': ['pubDate', 'expireDate']}),
        ('select_vote_config', {'fields': ['maxSelectCount']}),
        ('video_vote_config', {'fields': ['videoURL','videoLength']}),
    ]
    inlines = [EditOptions]
    vote_title = 'title'
    date_publish = 'pubDate'
    
@admin.register(VoteableUser)
class ManageVoteableUser(admin.ModelAdmin):
    list_display = ('id', 'userName', 'nickName')
@admin.register(FetchVote)
class ViewFetchVote(admin.ModelAdmin):
    list_display = ('userName', 'roomID', 'fetchDate')
    readonly_fields = ('userName', 'roomID', 'fetchDate')
@admin.register(VoteTicket)
class ViewVoteTicket(admin.ModelAdmin):
    list_display = ('roomID', 'roomVoteType', 'option_or_score', 'hashUserName', 'doneVideo')
    readonly_fields = ('roomID', 'roomVoteType', 'option_or_score', 'hashUserName', 'doneVideo')

admin.site.register_view('invoiceList', view=invoiceList)
