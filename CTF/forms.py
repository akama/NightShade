from django import forms
import re

from CTF.models import Challenge

class ChallengeScoreForm(forms.Form):
    submission = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': ' Flag'}))
    key = ''

    def __init__(self, *args, **kwargs):
        if 'key' in kwargs:
            self.key = kwargs.pop('key')
            self.regex_key = kwargs.pop('regex_key')
        super(ChallengeScoreForm, self).__init__(*args, **kwargs)


    def clean_submission(self):
        if self.regex_key:
            if re.search(self.key, self.cleaned_data['submission']) == None:
                raise forms.ValidationError("Flag is not correct.")

        else:
            if self.cleaned_data['submission'] != self.key:
                raise forms.ValidationError("Flag is not correct.")


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

