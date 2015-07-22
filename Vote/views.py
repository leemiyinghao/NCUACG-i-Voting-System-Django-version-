from django.shortcuts import render,redirect
from twython import Twython
from .models import VoteableUser, VoteList, FetchVote, VoteTicket, Options
from django.http import HttpResponse
from django.http import Http404
from django.conf import settings
from django.contrib.auth import authenticate, login, logout as django_logout
from django.contrib.auth import get_user_model
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse

#Twitter Login Part
def twitterAuth(request):
    twitter = Twython(settings.TWITTER_KEY, settings.TWITTER_SECRET)
    authProps = twitter.get_authentication_tokens(callback_url='http://127.0.0.1:8000/twitterlogin/callback')

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
    #check whether session exist
    try:
        sid = request.COOKIES['sessionid']
    except KeyError:
        return redirect("/twitterlogin/")
    #check whether has competence
    try:
        user=VoteableUser.objects.get(userName=request.session['userName'])
    except VoteableUser.DoesNotExist:
        del request.session['requestToken']
        return redirect("/twitterlogin/")
    except KeyError:
        request.session.clear()
        return redirect("/twitterlogin/")
    #main
    try:
        voteList = VoteList.objects.order_by('-expireDate')
    except VoteList.DoesNotExist:
        voteList = None
    fetchVote = None
    voted = [False]
    #check whether voted
    for vote in voteList:
        try:
            fetchVote=FetchVote.objects.filter(userName=request.session['userName']).filter(roomID=vote.id)
            if fetchVote != None:
                while True:
                    try:
                        voted[vote.id] = True
                        break
                    except IndexError:
                        voted.append(False)                
        except FetchVote.DoesNotExist:
            while True:
                try:
                    voted[vote.id] = False
                    break
                except IndexError:
                    voted.append(False)       
        except KeyError:
            return redirect("/twitterlogin/")
    context = {'voteList': voteList,'voted': voted}
    return render(request, 'Vote/index.html', context)

def selectVoteRoom(request,voteID):
    #check whether session exist
    try:
        sid = request.COOKIES['sessionid']
    except KeyError:
        return redirect("/twitterlogin/")
    #fetch vote
    try:
        fetchVote=FetchVote.objects.filter(userName=request.session['userName']).filter(roomID=voteID)
    except FetchVote.DoesNotExist:
        fetchVote=FetchVote()
        fetchVote.userName = request.session['userName']
        fetchVote.roomID = VoteList.objects.get(pk=voteID)
        fetchVote.fetchDate = datetime.datetime.now()
        fetchVote.save()
    except KeyError:
        return redirect("/twitterlogin/")
    #main
    try:
        vote = VoteList.objects.get(pk=voteID)
    except VoteList.DoesNotExist:
        raise Http404('Vote Room not found')
    try:
        optionList = Options.objects.filter(roomID=voteID)
    except Options.DoesNotExist:
        raise Http404('Option not found')
    context = {'vote': vote,'optionList': optionList}
    return render(request, 'Vote/selectVoteRoom.html', context)
    
def sendVote(request,voteID):
    #check whether session exist
    try:
        sid = request.COOKIES['sessionid']
    except KeyError:
        return redirect("/twitterlogin/")
    #main
    voteTicket = VoteTicket()
    voteTicket.roomID = VoteList.objects.get(pk=voteID)
    voteTicket.userName = request.session['userName']
    voteTicket.optionID = Options.objects.get(pk=request.POST['option'])
    voteTicket.save()
    return redirect("/")