from re import template
from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View
from django import forms

from .models import *
from .forms import *

# Create your views here.


def home(request):
    return render(request, 'blogs/home.html')

class DetailView(View):
    """
    Detail page of a record
    """
    template = 'blogs/detail.html'

    def get(self, request, record_id=None):
        if record_id is None:
            return HttpResponseNotFound()
        record = Record.objects.get(id=record_id)
        # comments = ...
        return render(request, template,
            context={'record': record})

    def post(self, request, record_id=None):
        ...



@method_decorator(login_required(login_url='/accounts/login'), name='dispatch')
class AllRecordView(View):
    """
    List all records
    """
    template = 'blogs/all_record.html'

    def get(self, request):
        srch = request.GET.get('search')
        if srch == '' or srch is None:
            want_list = list(Record.objects.filter(is_want=True))
            offer_list = list(Record.objects.filter(is_want=False))
        else:
            want_list = list(Record.objects.filter(is_want=True, want__icontains=srch))
            offer_list = list(Record.objects.filter(is_want=False, offer__icontains=srch))
        return render(request, self.template,
            context={'want_list': want_list, 'offer_list': offer_list})

    def post(self, request):
        ...


class NewWantView(View):
    """
    Create a new Want-Record
    """
    template = 'blogs/new_want.html' # 使用的模板
    success_redirect = '/' # 成功时重定向地址

    def get(self, request):
        form = Want_form()
        return render(request, self.template,
            context={'form': form})
            
    def post(self, request):
        form = Want_form(request.POST)
        if form.is_valid():
            new_want = form.save()
            return redirect(self.success_redirect)
        else:
            errors = {name:list(form.errors[name]) for name in form.errors}
            return render(request, self.template_name,
                context={'form': form, 'errors': errors})


class NewOfferView(View):
    """
    Create a new Offer-Record
    """
    template = 'blogs/new_offer.html' # 使用的模板
    success_redirect = '/' # 成功时重定向地址

    def get(self, request):
        form = Offer_form()
        return render(request, self.template,
            context={'form': form})
            
    def post(self, request):
        form = Offer_form(request.POST)
        if form.is_valid():
            new_want = form.save()
            return redirect(self.success_redirect)
        else:
            errors = {name:list(form.errors[name]) for name in form.errors}
            return render(request, self.template_name,
                context={'form': form, 'errors': errors})