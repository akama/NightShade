from django import forms
import re

from CTF.models import Challenge

'''
This takes a key (str), a regex flag (bool) and submission (string).
It compares the key to submission and returns True if matches or False if not.
'''
def check_submission(key, regex, submission):
    if regex and not re.search(key, submission) == None:
        return True 
    elif submission == key:
        return True 
    else:
        return False 


class BlindContestScoreForm(forms.Form):
    submission = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': ' Flag?'}))
    error_msg = "No such flag exists."

    def __init__(self, *args, **kwargs):
        self.challenges = kwargs.pop('challenges')

        super(BlindContestScoreForm, self).__init__(*args, **kwargs)

    def clean_submission(self):
        for challenge in self.challenges:
            # we need to check if any challenges matches
            if check_submission(challenge.key, challenge.regex_key, self.cleaned_data['submission']):
                self.challenge = challenge
                break
        # no challenge is correct.
        if not hasattr(self, 'challenge'):
            raise forms.ValidationError(self.error_msg)

    def sucessful_challenge(self):
        return self.challenge

class ChallengeScoreForm(forms.Form):
    submission = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': ' Flag?'}))
    key = ''
    error_msg = "Flag is not correct."

    def __init__(self, *args, **kwargs):
        if 'key' in kwargs:
            self.key = kwargs.pop('key')
            self.regex_key = kwargs.pop('regex_key')

        super(ChallengeScoreForm, self).__init__(*args, **kwargs)


    def clean_submission(self):
        if check_submission(self.key, self.regex_key, self.cleaned_data['submission']):
            # we don't need to do anything
            pass
        else:
            raise forms.ValidationError(self.error_msg)


class ChallengeAdminForm(forms.ModelForm):
    class Meta:
        model = Challenge
        exclude = []

    def clean(self):
        data = super(ChallengeAdminForm, self).clean()
        regex_flag = data.get("regex_key")
        key = data.get("key")

        if regex_flag:
            try:
                re.compile(key)
            except:
                raise forms.ValidationError("The regex isn't correct")

