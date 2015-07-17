from django.shortcuts import render, redirect
from django.http import Http404
from .models import Question, Choice
# Create your views here.
def index(request):
    question_list = Question.objects.order_by('-expire_date')
    context = {'question_list': question_list}
    return render(request, 'NormalVote/index.html', context)

def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404('Question not found') 
    try:
        choice = Choice.objects.filter(question=question_id)
    except Choice.DoesNotExist:
        raise Http404('Choice not found')
    return render(request, 'NormalVote/detail.html', {'question': question, 'choice': choice})

def invoice(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404('Question not found')
    try:
        choice = Choice.objects.filter(question=question_id)
    except Choice.DoesNotExist:
        raise Http404('Choice not found')
    return render(request, 'NormalVote/invoice.html', {'question': question, 'choice': choice})

def vote(requestion, question_id, vote_id):
    try:
        vote = Choice.objects.get(pk=vote_id)
        vote.votes += 1
        vote.save()
    except Choice.DoesNotExist:
        raise Http404('Choice not found')
    return redirect('/normalvote/'+question_id+'/')
