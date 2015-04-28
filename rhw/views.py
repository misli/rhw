from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.http import is_safe_url
from django.utils.text import slugify
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, FormView, CreateView

from .forms import *
from .models import *


class RhwsView(ListView):
    model = RedHackWeek



class RhwView(DetailView):
    model = RedHackWeek



class RhwCreateView(CreateView):
    model = RedHackWeek
    fields = ('title', 'slug', 'text', 'start', 'end', 'status')
    prepopulated_fields = {'slug': ('title',)}

    def get_form(self, form_class):
        form = super(RhwCreateView, self).get_form(form_class)
        for f in form.fields:
            form.fields[f].widget.attrs = {'class': 'form-control'}
        return form

    def form_valid(self, form):
        response = super(RhwCreateView, self).form_valid(form)
        self.object.ideas = Idea.objects.filter(redhackweeks=None)
        return response

    def get_context_data(self, **kwargs):
        context_data = super(RhwCreateView, self).get_context_data(**kwargs)
        context_data['prepopulated_fields'] = [{
            'field': context_data['form'][field_name],
            'dependencies': [context_data['form'][f] for f in dependencies]
        } for field_name, dependencies in self.prepopulated_fields.items()]
        return context_data


class RhwEditView(UpdateView):
    model = RedHackWeek
    fields = ('title', 'slug', 'text', 'start', 'end', 'status')

    def get_form(self, form_class):
        form = super(RhwEditView, self).get_form(form_class)
        for f in form.fields:
            form.fields[f].widget.attrs = {'class': 'form-control'}
        return form



class RhwNominateView(FormView):
    form_class = RhwNominateForm
    model = RedHackWeek
    template_name = 'rhw/redhackweek_nominate.html'

    def get_form(self, form_class):
        self.rhw = get_object_or_404(RedHackWeek, slug=self.kwargs['slug'], status=RedHackWeek.STATUS_IDEAS)
        form = super(RhwNominateView, self).get_form(form_class)
        form.fields['idea'].initial = None
        form.fields['idea'].choices = (
            (i.id, i.title) for i in Idea.objects.filter(project=None).exclude(redhackweeks=self.rhw)
        )
        form.fields['idea'].widget.attrs = {'class': 'form-control'}
        return form

    def get_context_data(self, **kwargs):
        context_data = super(RhwNominateView, self).get_context_data(**kwargs)
        context_data['redhackweek'] = self.rhw
        return context_data

    def form_valid(self, form):
        self.rhw.ideas.add(form.cleaned_data['idea'])
        return redirect(self.rhw.get_absolute_url())



class RhwNominateNewView(CreateView):
    model = Idea
    fields = ('title', 'slug', 'text')
    prepopulated_fields = {'slug': ('title',)}

    def get_form(self, form_class):
        self.rhw = get_object_or_404(RedHackWeek, slug=self.kwargs['slug'], status=RedHackWeek.STATUS_IDEAS)
        form = super(RhwNominateNewView, self).get_form(form_class)
        for f in form.fields:
            form.fields[f].widget.attrs = {'class': 'form-control'}
        return form

    def get_context_data(self, **kwargs):
        context_data = super(RhwNominateNewView, self).get_context_data(**kwargs)
        context_data['redhackweek'] = self.rhw
        context_data['prepopulated_fields'] = [{
            'field': context_data['form'][field_name],
            'dependencies': [context_data['form'][f] for f in dependencies]
        } for field_name, dependencies in self.prepopulated_fields.items()]
        return context_data

    def form_valid(self, form):
        idea = form.save(False)
        idea.created = date.today()
        idea.slug = slugify(idea.title)
        idea.save()
        idea.authors.add(self.request.user)
        self.rhw.ideas.add(idea)
        return redirect(self.rhw.get_absolute_url())



class RhwSelectView(CreateView):
    model = Project
    fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}

    def get_initial(self):
        self.rhw    = get_object_or_404(RedHackWeek, slug=self.kwargs['rhw'], status=RedHackWeek.STATUS_PROJECTS)
        self.idea   = get_object_or_404(Idea, slug=self.kwargs['idea'], redhackweeks=self.rhw, project=None)
        return {
            'rhw':      self.rhw,
            'idea':     self.idea,
            'title':    self.idea.title,
            'slug':     self.idea.slug,
            'text':     self.idea.text,
        }

    def get_form(self, form_class):
        form = super(RhwSelectView, self).get_form(form_class)
        for f in form.fields:
            form.fields[f].widget.attrs = {'class': 'form-control'}
        return form

    def get_context_data(self, **kwargs):
        context_data = super(RhwSelectView, self).get_context_data(**kwargs)
        context_data['redhackweek'] = self.rhw
        context_data['idea']        = self.idea
        context_data['prepopulated_fields'] = [{
            'field': context_data['form'][field_name],
            'dependencies': [context_data['form'][f] for f in dependencies]
        } for field_name, dependencies in self.prepopulated_fields.items()]
        return context_data

    def form_valid(self, form):
        project = form.save(False)
        project.rhw = self.rhw
        project.idea = self.idea
        project.save()
        project.members = self.idea.interested.all()
        return redirect(self.rhw.get_absolute_url())



class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self):
        return {
            'latest_rhw':   RedHackWeek.objects.first(),
        }



class IdeasView(ListView):
    model = Idea

    def get_queryset(self):
        return Idea.objects.filter(project=None).order_by('-id')



class IdeaView(DetailView):
    model = Idea



class IdeaCreateView(CreateView):
    model = Idea
    fields = ('title', 'slug', 'text')
    prepopulated_fields = {'slug': ('title',)}

    def form_valid(self, form):
        idea = form.save(False)
        idea.created = date.today()
        idea.save()
        idea.authors.add(self.request.user)
        return redirect(idea.get_absolute_url())

    def get_context_data(self, **kwargs):
        context_data = super(IdeaCreateView, self).get_context_data(**kwargs)
        context_data['prepopulated_fields'] = [{
            'field': context_data['form'][field_name],
            'dependencies': [context_data['form'][f] for f in dependencies]
        } for field_name, dependencies in self.prepopulated_fields.items()]
        return context_data



class IdeaEditView(UpdateView):
    model = Idea
    fields = ('title', 'slug', 'text', 'authors')

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Idea.objects
        else:
            return self.request.user.ideas

    def get_form(self, form_class):
        form = super(IdeaEditView, self).get_form(form_class)
        for f in form.fields:
            form.fields[f].widget.attrs = {'class': 'form-control'}
        return form



def interested(request, slug, op):
    idea = get_object_or_404(Idea, slug=slug)
    if op == '+':
        idea.interested.add(request.user)
    else:
        idea.interested.remove(request.user)
    return back(request, idea.get_absolute_url())



class ProjectsView(ListView):
    model = Project



class ProjectView(DetailView):
    model = Project



class ProjectEditView(UpdateView):
    model = Project
    fields = ('title', 'slug', 'text')

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Project.objects
        else:
            return self.request.user.projects

    def get_form(self, form_class):
        form = super(ProjectEditView, self).get_form(form_class)
        for f in form.fields:
            form.fields[f].widget.attrs = {'class': 'form-control'}
        return form



def member_vote(request, slug, op):
    project = get_object_or_404(Project, slug=slug, rhw__status__lte=RedHackWeek.STATUS_VOTING)
    if project.rhw.status == RedHackWeek.STATUS_VOTING:
        if request.user not in project.members.all():
            if op == '+':
                project.votes.add(request.user)
            else:
                project.votes.remove(request.user)
    else:
        if op == '+':
            project.members.add(request.user)
        else:
            project.members.remove(request.user)
    return back(request, project.get_absolute_url())



def back(request, default_redirect='/'):
    redirect_to = request.REQUEST.get('back', default_redirect)
    if not is_safe_url(url=redirect_to, host=request.get_host()):
        redirect_to = default_redirect
    return redirect(redirect_to)

