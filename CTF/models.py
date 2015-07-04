from hashlib import md5
from random import random
from operator import itemgetter

from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.template.defaultfilters import slugify


class Score(models.Model):
    user = models.ForeignKey(User)
    challenge = models.ForeignKey('Challenge')
    completed = models.DateTimeField(auto_now_add=True)
    contest = models.ForeignKey('Contest')

    def __str__(self):
        return "{0}:{1} for {2} points".format(self.challenge, self.user, self.challenge.points)

    def get_points(self):
        return self.challenge.points


class ScoreAdmin(admin.ModelAdmin):
    pass


admin.site.register(Score, ScoreAdmin)


class Contest(models.Model):
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    slug = models.SlugField(max_length=200, unique=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def score_board(self):
        results = self.score_set.all()
        sorted_results = []
        found_match = False
        for score in results:
            for foo in sorted_results:
                if score.user.username == foo[0]:
                    foo[1] = foo[1] + score.get_points()
                    if score.completed > foo[2]:
                        foo[2] = score.completed
                    found_match = True
            if not found_match:
                sorted_results.append([score.user.username, score.get_points(), score.completed])
            found_match = False

        # sorting bitches
        sorted_results.sort(key=itemgetter(2))
        sorted_results.sort(key=itemgetter(1), reverse=True)

        return sorted_results

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)

        super(Contest, self).save(*args, **kwargs)


class ContestAdmin(admin.ModelAdmin):
    exclude = ('slug'),


admin.site.register(Contest, ContestAdmin)


class Challenge(models.Model):
    contest = models.ForeignKey(Contest)
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    category = models.CharField(max_length=200)
    description = models.TextField()
    points = models.IntegerField()
    key = models.CharField(max_length=20, default=md5(str(random()).encode()).hexdigest()[:8].upper())
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)

        super(Challenge, self).save(*args, **kwargs)

    def solved(self, user):
        try:
            self.score_set.get(user=user).user
            return True
        except Score.DoesNotExist:
            return False
        except TypeError:
            return False


class ChallengeAdmin(admin.ModelAdmin):
    exclude = ('slug'),


admin.site.register(Challenge, ChallengeAdmin)


