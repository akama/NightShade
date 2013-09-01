from hashlib import md5
from random import random

from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.template.defaultfilters import slugify



# Create your models here.
class Contest(models.Model):
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    slug = models.SlugField(max_length=200, unique=True)
    active = models.BooleanField()

    def __str__(self):
        return self.title

    def score_board(self):
        results = dict()
        for chal in self.challenge_set.all():
            for sc in chal.score_set.all():
                if sc.user.__str__() in results:
                    results[sc.user.__str__()] = results[sc.user.__str__()] + sc.get_points()
                else:
                    results[sc.user.__str__()] = + sc.get_points()
        return results

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
    active = models.BooleanField()

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


class ChallengeAdmin(admin.ModelAdmin):
    exclude = ('slug'),


admin.site.register(Challenge, ChallengeAdmin)


class Score(models.Model):
    user = models.ForeignKey(User)
    challenge = models.ForeignKey(Challenge)

    def __str__(self):
        return "{0}:{1} for {2} points".format(self.challenge, self.user, self.challenge.points)

    def get_points(self):
        return self.challenge.points


class ScoreAdmin(admin.ModelAdmin):
    pass


admin.site.register(Score, ScoreAdmin)

