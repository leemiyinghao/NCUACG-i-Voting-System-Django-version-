from django import template

register = template.Library()

@register.filter
def hasUserFetchVote(vote, userName):
    return vote.hasUserFetchVote(userName)

@register.filter
def hasSelectOption(userName, optionID):
    return VoteTicket.objects.filter(userName=userName, optionID = optionID).exists()
