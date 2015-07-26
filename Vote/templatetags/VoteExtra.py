from django import template

register = template.Library()

@register.filter
def hasUserFetchVote(vote, userName):
    return vote.hasUserFetchVote(userName)

@register.filter
def hasUserVoteThisOption(userName, option):
    return option.hasUserVoteThisOption(userName)
