from django.contrib.auth.forms import UserCreationForm

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.views.generic.detail import DetailView
from django.views.generic import FormView, View
from django.views.generic.detail import SingleObjectMixin

from CTF.models import Contest, Challenge

from CTF.forms import ChallengeScoreForm



# Create your views here.

@login_required
def current_datetime(request):
    if request.user.is_authenticated():
        return render(request, 'time.html', context_instance=RequestContext(request))


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect(reverse('home'))
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {
        'form': form,
    })


@login_required
def profile(request):
    return HttpResponseRedirect(reverse('home'))


class ChallengeDetail(View):
    def get(self, request, *args, **kwargs):
        view = ChallengeDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = ChallengePost.as_view()
        return view(request, *args, **kwargs)


class ChallengeDisplay(DetailView):
    model = Challenge

    def get_context_data(self, **kwargs):
        context = super(ChallengeDisplay, self).get_context_data(**kwargs)
        context['form'] = ChallengeScoreForm()
        return context


class ChallengePost(SingleObjectMixin, FormView):
    template_name = 'CTF/challenge_detail.html'
    form_class = ChallengeScoreForm
    model = Challenge

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('login')
        self.object = self.get_object()
        return super(ChallengePost, self).post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('home')


'''
class ChallengeDetailView(FormMixin, DetailView):
    model = Challenge
    form_class = ChallengeScoreForm

    def get_success_url(self):
        return reverse('home')

    def get_context_data(self, **kwargs):
        context = super(ChallengeDetailView, self).get_context_data(**kwargs)
        form_class = self.get_form_class()
        context['form'] = self.get_form_class()
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('home'))
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            print(form.cleaned_data['submission'] + self.object.key)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        return super(ChallengeDetailView, self).form_valid(form)
'''


class ContestDetailView(DetailView):
    model = Contest

    def get_context_data(self, **kwargs):
        return super(ContestDetailView, self).get_context_data(**kwargs)
