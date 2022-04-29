from django.urls import path
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_view
from django.contrib.auth import authenticate, login
from django.views.generic import View
from .forms import *    

# Create your views here.
class LoginViewClass(View):
    template = 'accounts/login.html'
    redirect_authenticated_user = True

    def get(self, request):
        form = LoginForm()
        next = request.GET.get("next")
        return render(request, self.template, {'form': form, 'next': next})

    def post(self, request):
        form = LoginForm(request.POST)
        next = form.data.get('next') # It's a STRING
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username,password=password)

            if user and user.is_active: 
                login(request,user)
                request.session["username"] = username 
                return HttpResponseRedirect(self.get_redirect_url(next))

            elif user and not user.is_active:
                print(user, 'not active')
                pass
            else:
                return render(request, self.template, 
                    {'form': LoginForm(), 'error_msg': 'Failed to login. Check your username and password.'})
        else:
            return render(request, self.template, 
                    {'form': LoginForm(), 'error_msg': 'Failed to login. Invalid Input.'})
                
    def get_redirect_url(self, next=None) -> str: 
        if next == 'None':
            return '/'
        else:
            return str(next)

class RegisterViewClass(View):
    """
    Class-based view for user register
    """
    template = 'accounts/register.html'
    redirect_authenticated_user = True

    def get(self, request):
        form = UserCreationForm()
        #for item in form:
            #print(item) # <input type="text" name="date_of_birth" required id="id_date_of_birth">
            #print(item.name) # date_of_birth
        next = request.GET.get("next")
        return render(request, self.template, {'form': form, 'next': next})

    def post(self, request):
        form = UserCreationForm(request.POST)
        next = form.data.get('next')
        if next == '':
            next = None
        if form.is_valid():
            new_user = form.save()
            login(request,new_user)
            return redirect(self.get_redirect_url(next))
        else:
            errors = {name:list(form.errors[name]) for name in form.errors}
            for i in errors:
                print(i, errors[i])
            return render(request, self.template,
                context={'form': form, 'error_msg': 'Invalid input', 'errors': errors})


    def get_redirect_url(self, next=None) -> str: 
        if next == 'None' or next is None:
            return '/'
        else:
            return str(next)

class UserinfoViewClass(View):
    template = 'accounts/userinfo.html'
    redirect_authenticated_user = True

    def get(self, request):
        user = request.user
        form = UserChangeForm(instance=user)
        print(form)
        next = request.GET.get("next")
        return render(request, self.template, {'form': form, 'next': next})

    def post(self, request):
        user = request.user
        form = UserChangeForm(instance=user,data=request.POST)
        print(user)
        next = form.data.get('next')
        if next == '':
            next = None
        if form.is_valid():
            print(user)
            form.save()
            return redirect(self.get_redirect_url(next))
        else:
            errors = {name:list(form.errors[name]) for name in form.errors}
            return render(request, self.template,
                context={'form': form, 'error_msg': 'Invalid input', 'errors': errors})


    def get_redirect_url(self, next=None) -> str: 
        if next == 'None' or next is None:
            return '/'
        else:
            return str(next)