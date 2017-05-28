from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login

from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import redirect
from django.contrib.auth.models import User

from CTF.models import Contest, Challenge, Score

from CTF.forms import ChallengeScoreForm, BlindContestScoreForm

import json

# Create your views here.

@login_required
def current_datetime(request):
    if request.user.is_authenticated():
        return render(request, 'time.html')


def home_page(request):
    contests = []

    for contest in Contest.objects.all():
        if contest.active:
            contests.append(contest)

    if len(contests) == 1:
        return redirect(reverse('contest-view', args=(contests[0].slug,)))

    return render(request, 'home.html', {'contests': contests}, )


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],)
            login(request, new_user)
            return HttpResponseRedirect(reverse('home'))
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {
        'form': form,
    })


def profile(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist as e:
        raise Http404("User does not exist.")

    user_score_set = user.score_set.all()
    contests = []
    results = {}

    for score in user_score_set:
        if score.contest not in contests:
            contests.append(score.contest)

    for contest in contests:
        scores_for_contest = []
        total_score = 0
        for score in user_score_set:
            if score.contest == contest:
                scores_for_contest.append(score)
                total_score += score.challenge.points
        results[contest] = (scores_for_contest, total_score)

    return render(request, 'CTF/profile.html', {'object': user, 'challenges': results})


def ChallengeView(request, slug):
    challenge = Challenge.objects.get(slug=slug)

    if request.method == 'POST' and not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))

    if request.method == 'POST':
        kwargs = {'key': challenge.key, 'regex_key': challenge.regex_key}
        form = ChallengeScoreForm(request.POST, **kwargs)
        if form.is_valid() and not challenge.solved(request.user) and challenge.contest.active and challenge.active:
            score = Score(challenge=challenge, user=request.user, contest=challenge.contest)
            score.save()
            return HttpResponseRedirect(reverse('challenge-view', args=(slug,)))
    else:
        form = ChallengeScoreForm()

    solved = challenge.solved(request.user)

    return render(request, 'CTF/challenge_detail.html',
                  {'object': challenge, 'form': form, 'solved': solved,
                   'files': challenge.challengefile_set.all()})


def ContestView(request, slug):
    try:
        contest = Contest.objects.get(slug=slug)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('home_page'))




    if contest.contest_type == Contest.JEOPARDY:
        return jeopardy_view(request, slug)
    elif contest.contest_type == Contest.BLIND:
        return blind_view(request, slug)
    else:
        return listing_view(request, slug)

def listing_view(request, slug):
    contest = Contest.objects.get(slug=slug)
    challenges = []
    if request.user.is_authenticated():
        challenges = [(challenge, challenge.solved(request.user)) for challenge in contest.challenge_set.all()]
    else:
        challenges = [(challenge, False) for challenge in contest.challenge_set.all()]
    return render(request, 'CTF/contest_detail.html',
                    {'challenges': challenges, 'object': contest})

def jeopardy_view(request, slug):
    contest = Contest.objects.get(slug=slug)
    catagories = {}
    challenges = contest.challenge_set.all()
    for challenge in challenges:
        # Add if the user has solved the challenge or not
        if request.user.is_authenticated and challenge.solved(request.user):
            challenge_to_add = (challenge, True)
        else:
            challenge_to_add = (challenge, False)

        # Add challenge to category
        if challenge.category not in catagories:
            catagories[challenge.category] = [challenge_to_add]
        else:
            catagories[challenge.category].append(challenge_to_add)

    for category, challenges in catagories.iteritems():
        challenges.sort(key=lambda challenge_and_score: challenge_and_score[0].points)


    return render(request, 'CTF/contest_detail_jeopardy.html',
                    {'catagories': catagories, 'object': contest})

def blind_view(request, slug):
    contest = Contest.objects.get(slug=slug)

    challenges = contest.challenge_set.all()

    if request.method == 'POST' and not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))

    if request.method == 'POST':
        kwargs = {'challenges': challenges}
        form = BlindContestScoreForm(request.POST, **kwargs)
        if form.is_valid() and not form.sucessful_challenge().solved(request.user):
            score = Score(challenge=form.sucessful_challenge(), user=request.user, contest=form.sucessful_challenge().contest)
            score.save()
            messages.add_message(request, messages.SUCCESS, 'Challenge Solved!')
            return HttpResponseRedirect(reverse('contest-view', args=(slug,)))
        if form.is_valid() and form.sucessful_challenge().solved(request.user):
            messages.add_message(request, messages.SUCCESS, 'This challenge was already solved.')
            return HttpResponseRedirect(reverse('contest-view', args=(slug,)))
    else:
        form = ChallengeScoreForm()

    check = lambda x: not x.solved(request.user)
    # stores if all the challenges have been solved
    solved = any(check(x) for x in challenges)

    return render(request, 'CTF/contest_detail_blind.html',
            {'object': contest, 'form' : form, 'solved' : solved})

def health(request):
    return HttpResponse(status=200)

def ctftime_endpoint(request, slug):
    scores = []
    contest = Contest.objects.get(slug=slug)
    for i, score in enumerate(contest.score_board()):
        scores.append({"pos": i+1, "team": score[0], "score": score[1]})
    return HttpResponse(json.dumps({"standings": scores}))
