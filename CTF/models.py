from hashlib import md5
from random import random
from operator import itemgetter

from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.template.defaultfilters import slugify
from django.dispatch import receiver


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
    LISTING = "L"
    JEOPARDY = "J"

    CONTEST_TYPES_CHOICES = (
        (LISTING, "Listing"),
        (JEOPARDY, "Jeopardy"),
    )

    title = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    slug = models.SlugField(max_length=200, unique=True)
    active = models.BooleanField(default=False)
    contest_type = models.CharField(max_length=1, choices=CONTEST_TYPES_CHOICES, default=LISTING)

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


def genRandomFlag():
    return md5(str(random()).encode()).hexdigest()[:16].upper()


class Challenge(models.Model):
    contest = models.ForeignKey(Contest)
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    category = models.CharField(max_length=200)
    description = models.TextField()
    points = models.IntegerField()
    key = models.CharField(max_length=200, default=genRandomFlag)
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


def challengeFilePath(instance, filename):
    return '%s/%s' % (instance.challenge.title, filename)


class ChallengeFile(models.Model):
    challenge = models.ForeignKey(Challenge)
    fileObject = models.FileField(upload_to=challengeFilePath)

    def __str__(self):
        if self.fileObject:
            return self.fileObject.name.split('/')[-1].replace(' ', '_')
        else:
            return 'None'


@receiver(models.signals.post_delete, sender=ChallengeFile)
def remove_file_from_s3(sender, instance, using, **kwargs):
    instance.fileObject.delete(save=False)


class ChallengeFileAdmin(admin.StackedInline):
    model = ChallengeFile
    extra = 3


class ChallengeAdmin(admin.ModelAdmin):
    exclude = [('slug'), ]
    inlines = [ChallengeFileAdmin]

admin.site.register(Challenge, ChallengeAdmin)
