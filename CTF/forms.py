from django import forms


def get_challenge_form(challenge):
    "Return the form for a specific challenge"

    challenge_key = challenge.key

    class ChallengeForm(forms.Form):
        def __init__(self, *args, **kwargs):
            forms.Form.__init__(self, *args, **kwargs)
            self.key = challenge_key

        def save(self):
            print()


class ChallengeScoreForm(forms.Form):
    submission = forms.CharField(max_length=10)

    def clean_submission(self):
        if self.cleaned_data['submission'] != "testing":
            print("Flag is not correct")
            raise forms.ValidationError("Flag is not correct.")
