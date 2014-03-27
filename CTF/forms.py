from django import forms


class ChallengeScoreForm(forms.Form):
    submission = forms.CharField(max_length=16)
    key = ''

    def __init__(self, *args, **kwargs):
        if 'key' in kwargs:
            self.key = kwargs.pop('key')
        super(ChallengeScoreForm, self).__init__(*args, **kwargs)


    def clean_submission(self):
        if self.cleaned_data['submission'] != self.key:
            raise forms.ValidationError("Flag is not correct.")
