from django.shortcuts import render, redirect
from django.urls import reverse_lazy 

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Task


# CRUD using CBV 
class TaskList(LoginRequiredMixin, ListView) : 
    model = Task

    context_object_name = 'Tasks'

    # if we wanna add context data or modify the existing(tasks)
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs) 
        context['Tasks'] = context['Tasks'].filter(user = self.request.user)
        context['count'] = context['Tasks'].filter(completed = False).count()
        search_input = self.request.GET.get('search') or ''
        if search_input : 
            context['Tasks'] =  context['Tasks'].filter(
                title__icontains = search_input)

        context['search_par'] = search_input 

        return context


class Detail(LoginRequiredMixin,DetailView): 
    model = Task 
    context_object_name = 'task'
    #template_name = "base/task_list"
class Create(LoginRequiredMixin,CreateView): 
    model = Task 
    fields = ['title', 'description', 'completed']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form) : 
        form.instance.user = self.request.user 
        return super(Create, self).form_valid(form)
class Update(LoginRequiredMixin,UpdateView):
    model = Task 
    fields = ['title', 'description', 'completed']
    success_url = reverse_lazy('tasks')
class Delete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')

# login/logout/register
class Login(LoginView):
    template_name = "base/login.html"
    fields = "__all__"
    redirect_authenticated_user = True 

    def get_success_url(self) : 
        return reverse_lazy("tasks")
# logout used directly in urls file 
class Register(FormView):
    template_name = "base/register.html"
    form_class =UserCreationForm
    redirect_authenticated_user = True 
    success_url = reverse_lazy('tasks')

    def form_valid(self, form): 
        user = form.save()
        if user is not None : 
            login(self.request,user )
        return super(Register, self).form_valid(form)
    def get(self, *args , **kwargs):
        if self.request.user.is_authenticated:
            return redirect("tasks")
        return super(Register, self).get( *args , **kwargs)
