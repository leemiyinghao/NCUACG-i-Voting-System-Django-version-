from django.contrib import admin
from .models import VoteList, VoteableUser, FetchVote, VoteTicket, Options
# Register your models here.

admin.site.register(VoteList)
admin.site.register(VoteableUser)
admin.site.register(FetchVote)
admin.site.register(VoteTicket)
admin.site.register(Options)
