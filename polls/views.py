from django.shortcuts import render,redirect
from authomatic import Authomatic
from authomatic.adapters import DjangoAdapter
from django.http import HttpResponse

from config import CONFIG

authomatic = Authomatic(CONFIG, 'howdoyouturnthison')

#Twitter Login Part
def twitterlogin(request):
    response = HttpResponse()
    result = authomatic.login(DjangoAdapter(request, response), "twitter")
    if result:
        if result.error:
            #display twitterLoginError
            return render(request, 'polls/error.html', {'error_type': "Twitter Login Error"})
        elif result.user:
            if not (result.user.name and result.user.id):
                result.user.update()

            #update username into session stroge
            request.session['username'] = result.user.name

            #redirect to login
            return redirect('/login/')

#Write rest of code here
