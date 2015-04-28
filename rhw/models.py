from ckeditor.fields import RichTextField
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Idea(models.Model):
    title       = models.CharField(max_length=100, unique=True)
    slug        = models.SlugField(unique=True)
    text        = RichTextField(blank=True)
    created     = models.DateField()
    authors     = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='ideas')
    interested  = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='interested', blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('idea', args=(self.slug,))



@python_2_unicode_compatible
class RedHackWeek(models.Model):
    STATUS_IDEAS    = 1
    STATUS_PROJECTS = 2
    STATUS_HACKING  = 3
    STATUS_VOTING   = 4
    STATUS_CLOSED   = 5

    STATUS_CHOICES  = {
        STATUS_IDEAS:   'collecting ideas',
        STATUS_PROJECTS:'creating list of approved projects',
        STATUS_HACKING: 'hacking',
        STATUS_VOTING:  'voting',
        STATUS_CLOSED:  'closed',
    }

    title   = models.CharField(max_length=100)
    slug    = models.SlugField(unique=True)
    text    = RichTextField(blank=True)
    start   = models.DateField()
    end     = models.DateField()
    ideas   = models.ManyToManyField(Idea, blank=True, related_name='redhackweeks')
    status  = models.IntegerField(max_length=10, choices=STATUS_CHOICES.items(), default=STATUS_IDEAS)

    class Meta:
        ordering = ('-start',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('rhw', args=(self.slug,))

    def get_status(self):
        return self.STATUS_CHOICES[self.status]

    @property
    def unselected_ideas(self):
        return self.ideas.exclude(project__rhw=self)


@python_2_unicode_compatible
class Project(models.Model):
    idea    = models.OneToOneField(Idea, related_name='project')
    rhw     = models.ForeignKey(RedHackWeek, related_name='projects')
    title   = models.CharField(max_length=100, unique=True)
    slug    = models.SlugField(unique=True)
    text    = RichTextField(blank=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='projects', blank=True)
    votes   = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='votes', blank=True)

    def __str__(self):
        return self.idea.title

    def get_absolute_url(self):
        return reverse('project', args=(self.slug,))


