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
import hashlib
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

def index(request):
    userName = request.session.get('userName',None)
    if userName == None:
        return render(request, "Vote/indexNonLogin.html", )
    elif not VoteableUser.objects.filter(userName = userName).exists():
        return HttpResponse("Permission denied")
    voteList = VoteList.objects.filter(expireDate__gt = (timezone.now() - timedelta(days=3))).order_by('-expireDate')
    today = timezone.now()
    finish = VoteList.objects.filter(pk=request.GET.get('finish')).first() if request.GET.get('finish') else None
    error = request.GET.get('error')
    return render(request, "Vote/index.html", {'voteList': voteList, 'userName': userName, 'today': today, 'finish': finish, 'error': error})

def voteRoom(request, voteID):
    userName = request.session.get('userName', None)
    if userName == None:
        return redirect("/")
    elif not VoteableUser.objects.filter(userName = userName).exists():
        return redirect("/")
    vote = get_object_or_404(VoteList, pk = voteID)
    sha1 = hashlib.sha1()
    sha1.update((userName + "." + vote.hashSetKey).encode('utf-8'))
    hashId = sha1.hexdigest()[:10]
    optionList = Options.objects.filter(roomID = voteID)
    voted = VoteTicket.objects.filter(hashUserName = hashId, roomID = voteID).exists()
    fetchVote = FetchVote(userName = userName, roomID = vote, fetchDate = timezone.now())
    fetchVote.save()
    error = request.GET.get('error','')
    if vote.voteType == 'v':
        score = 0 if VoteTicket.objects.filter(hashUserName = hashId, roomID = voteID).last()==None else VoteTicket.objects.filter(hashUserName = hashId, roomID = voteID).last().score
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
    sha1 = hashlib.sha1()
    sha1.update((userName + "." + vote.hashSetKey).encode('utf-8'))
    hashId = sha1.hexdigest()[:10]
    if vote.expireDate < timezone.now():
        return redirect("/?error=overtimevote")
    if vote.voteType == "v":
        doneVideo = not request.POST.get('hasDoneTheVideo')==None
        fetchVote = FetchVote.objects.filter(userName = userName, roomID = vote.id).last()
        doneVideo = False if (fetchVote.fetchDate + timedelta(vote.videoLength)) > timezone.now() else doneVideo
        if request.POST.get('score') == None:
            return redirect("/voteroom/%s/?error=nonescore" % voteID)
        VoteTicket.objects.filter(hashUserName = hashId, roomID=vote.id).update(mute=True)
        voteTicket = VoteTicket(roomID = vote, score = request.POST.get('score'), doneVideo = doneVideo, hashUserName = hashId)
        voteTicket.save()
        return redirect("/?finish=%s" % voteID)
    else:
        optionList = Options.objects.filter(roomID = voteID)
        if vote.maxSelectCount > 1:
            optionNum = 0
            for option in optionList:
                if request.POST.get("option_%d" % option.id) == 'True':
                    optionNum += 1
            if optionNum > vote.maxSelectCount:
                return redirect("/voteroom/%s/?error=toomanyoption" % voteID)
            VoteTicket.objects.filter(userName=userName, roomID=vote.id).update(mute=True)
            for option in optionList:
                if request.POST.get("option_%d" % option.id) == 'True':
                    voteTicket = VoteTicket(roomID = vote, userName = userName, optionID = option, hashUserName = hashId)
                    voteTicket.save()
        elif not request.POST.get('option') == None:
            option = get_object_or_404(Options, pk=request.POST.get('option'))
            VoteTicket.objects.filter(userName=userName, roomID=vote.id).update(mute=True)
            voteTicket = VoteTicket(roomID = vote, userName = userName, optionID = option, hashUserName = hashId)
            voteTicket.save()
        return redirect("/?finish=%s" % voteID)
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

class Invoice(object):
    def __init__(self, hashSetKey):
        self.voteList = VoteList.objects.filter(hashSetKey = hashSetKey).order_by('pubDate')
        self.date = self.voteList[0].pubDate
        self.title = hashSetKey
def invoiceList(request):
    invoices = []
    for voteSet in VoteList.objects.values('hashSetKey').distinct():
        hashSetKey = voteSet['hashSetKey']
        invoices.append(Invoice(hashSetKey))
    return render(request, "Invoice/invoiceList.html", {'title': '票數統計',
                                                        'invoices': invoices})
def invoice(request, hashSetKey):
    votes = VoteList.objects.filter(hashSetKey=hashSetKey)
    voteTitles = [vote.title for vote in votes]
    voteTickets = VoteTicket.objects.filter(roomID__in=votes, mute=False)
    users = [i['hashUserName'] for i in voteTickets.values('hashUserName').distinct()]
    oriVoteSta = {}
    for user in users:
        temp = {}
        for voteTicket in VoteTicket.objects.filter(hashUserName = user):
            temp[voteTicket.roomID.title] = int(voteTicket.score)
        oriVoteSta[user] = temp
    normVoteSta = {}
    for user in users:
        normVoteSta[user] = {}
        sum = 0
        count = 0
        for voteTitle in oriVoteSta[user]:
            sum += oriVoteSta[user][voteTitle]
            count += 1
        factor = 2*count/sum
        for voteTitle in oriVoteSta[user]:
            normVoteSta[user][voteTitle] = oriVoteSta[user][voteTitle] * factor
    oriVoteTable = []
    normVoteTable = []
    for user in users:
        oriTemp = [user]
        normTemp = [user]
        for voteTitle in voteTitles:
            if voteTitle in oriVoteSta[user]:
                oriTemp.append("{:.5f}".format(oriVoteSta[user][voteTitle]))
                normTemp.append("{:.5f}".format(normVoteSta[user][voteTitle]))
            else:
                oriTemp.append('')
                normTemp.append('')
        oriVoteTable.append(oriTemp)
        normVoteTable.append(normTemp)
    fetchUsers = [fetch['userName'] for fetch in FetchVote.objects.filter(roomID__in=votes).values('userName').distinct()]
    return render(request, "Invoice/invoice.html", {'title': hashSetKey,
                                                    'oriVoteTable': oriVoteTable,
                                                    'normVoteTable': normVoteTable,
                                                    'voteTitleTable': voteTitles,
                                                    'fetchUsers': fetchUsers})
