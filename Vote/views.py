from django.shortcuts import render,redirect
from twython import Twython
from .models import VoteableUser, VoteList, FetchVote, VoteTicket, Options
from django.http import HttpResponse
from django.http import Http404
from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from datetime import timedelta, datetime
from django.utils import timezone

#Twitter Login Part
def twitterAuth(request):
    twitter = Twython(settings.TWITTER_KEY, settings.TWITTER_SECRET)
    authProps = twitter.get_authentication_tokens()
    request.session['requestToken'] = authProps
    return redirect(authProps['auth_url'])

def twitterCallback(request):
    oauthToken = request.session['requestToken']['oauth_token']
    oauthTokenSecret = request.session['requestToken']['oauth_token_secret']
    twitter = Twython(settings.TWITTER_KEY, settings.TWITTER_SECRET, oauthToken, oauthTokenSecret)
    authorizedTokens = twitter.get_authorized_tokens(request.GET['oauth_verifier'])
    request.session['userName'] = authorizedTokens['screen_name']
    return redirect("/login/")

# Write the rest of code here
def index(request):
    userName = request.session.get('userName',None)
    if userName == None:
        return render(request, "Vote/indexNonLogin.html", )
    elif not VoteableUser.objects.filter(userName = userName).exists():
        return HttpResponse("Permission denied")
    voteList = VoteList.objects.filter(expireDate__gt = (timezone.now() - timedelta(days=3))).order_by('-expireDate')
    today = timezone.now()
    return render(request, "Vote/index.html", {'voteList': voteList, 'userName': userName, 'today': today})

def voteRoom(request, voteID):
    userName = request.session.get('userName', None)
    if userName == None:
        return redirect("/")
    elif not VoteableUser.objects.filter(userName = userName).exists():
        return redirect("/")
    vote = get_object_or_404(VoteList, pk = voteID)
    optionList = Options.objects.filter(roomID = voteID)
    voted = VoteTicket.objects.filter(userName = userName, roomID = voteID).exists()
    fetchVote = FetchVote(userName = userName, roomID = vote, fetchDate = timezone.now())
    fetchVote.save()
    error = request.GET.get('error','')
    if vote.voteType == 'v':
        score = 0 if VoteTicket.objects.filter(userName = userName, roomID = voteID).last()==None else VoteTicket.objects.filter(userName = userName, roomID = voteID).last().score
        return render(request, 'Vote/videoVoteRoom.html', {'vote': vote,'optionList': optionList, 'userName': userName, 'voted': voted, 'score': score, 'error': error})
    else:
        return render(request, 'Vote/selectVoteRoom.html', {'vote': vote,'optionList': optionList, 'userName': userName, 'voted': voted, 'error': error})

def sendVote(request, voteID):
    userName = request.session.get('userName', None)
    if userName == None:
        return redirect("/")
    elif not VoteableUser.objects.filter(userName = userName).exists():
        return redirect("/")
    vote = get_object_or_404(VoteList, pk = voteID)
    if vote.voteType == "v":
        doneVideo = not request.POST.get('hasDoneTheVideo')==None
        if request.POST.get('score') == None:
            return redirect("/voteroom/%s/?error=nonescore" % voteID)
        voteTicket = VoteTicket(roomID = vote, userName = userName, score = request.POST.get('score'), doneVideo = doneVideo)
        voteTicket.save()
        return redirect("/")
    else:
        optionList = Options.objects.filter(roomID = voteID)
        if vote.maxSelectCount > 1:
            optionNum = 0
            for option in optionList:
                if request.POST.get("option_%d" % option.id) == 'True':
                    optionNum += 1
            if optionNum > vote.maxSelectCount:
                return redirect("/voteroom/%s/?error=toomanyoption" % voteID)
            for option in optionList:
                if request.POST.get("option_%d" % option.id) == 'True':
                    voteTicket = VoteTicket(roomID = vote, userName = userName, optionID = option)
                    voteTicket.save()
        elif not request.POST.get('option') == None:
            option = get_object_or_404(Options, pk=request.POST.get('option'))
            voteTicket = VoteTicket(roomID = vote, userName = userName, optionID = option)
            voteTicket.save()
        return redirect("/")
def login(request):
    userName = request.session.get('userName', None)
    if userName == None:
        return redirect("/twitterlogin/")
    elif VoteableUser.objects.filter(userName = userName).exists():
        return redirect("/")
    else:
        request.session['userName'] = None
        return render(request, "Vote/permissionNotAllow.html")
def logout(request):
    request.session['userName'] = None
    return redirect("/")
