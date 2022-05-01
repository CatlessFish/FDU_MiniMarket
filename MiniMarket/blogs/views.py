from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View
from django import forms
from accounts.models import SiteUser

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
        subscription_list = Subscribe.objects.filter(record=record)
        try:
            Subscribe.objects.get(record=record, created_by=request.user)
            interested = True
        except Subscribe.DoesNotExist:
            interested = False
        return render(request, self.template,
            context={'record': record, 'record_id': record_id, 'interested':interested,
            'subscription_list': subscription_list})

    def post(self, request, record_id=None):
        form = forms.Form(request.POST)
        user_id = form.data.get('user_id')
        rec_id = form.data.get('record_id')
        comment = form.data.get('comment')
        operation = form.data.get('operation')

        user = SiteUser.objects.get(id = int(user_id))
        record = Record.objects.get(id = int(rec_id))
        if comment is None:
            comment = ''
        
        if operation == 'subscribe':
            sub = Subscribe(created_by=user, record=record, comment=comment)
            sub.save()
        elif operation == 'unsubscribe':
            sub = Subscribe.objects.get(created_by=user, record=record)
            sub.delete()
        elif operation == 'close':
            record.is_active = False
            record.save()
        elif operation == 'reopen':
            record.is_active = True
            record.save()
        return redirect('/detail/'+str(rec_id)+'/')

#TODO  删帖


@method_decorator(login_required(login_url='/accounts/login'), name='dispatch')
class AllRecordView(View):
    """
    List all records
    """
    template = 'blogs/all_record.html'

    def get(self, request):
        srch = request.GET.get('search')
        all_wants = Record.objects.filter(is_want=1, is_active=True).order_by('-update_time')
        all_offers = Record.objects.filter(is_want=0, is_active=True).order_by('-update_time')
        print(all_wants)
        print(all_offers)
        if srch == '' or srch is None:
            want_list = list(all_wants)
            offer_list = list(all_offers)
        else:
            want_list = list(all_wants.filter(want__icontains=srch))
            offer_list = list(all_offers.filter(offer__icontains=srch))
        return render(request, self.template,
            context={'want_list': want_list, 'offer_list': offer_list, 'srch': srch})

    def post(self, request):
        ...


class NewWantView(View):
    """
    Create a new Want-Record
    """
    template = 'blogs/new_want.html' # 使用的模板
    success_redirect = 'blogs:all_record' # 成功时重定向地址

    def get(self, request):
        form = Want_form()
        return render(request, self.template,
            context={'form': form})
            
    def post(self, request):
        form = Want_form(request.POST)
        user_id = form.data.get('user_id')
        want = form.data.get('want')
        offer = form.data.get('offer')
        note = form.data.get('note')
        user = SiteUser.objects.get(id = user_id)
        record = Record(is_want=1, want=want, offer=offer, note=note, created_by=user)
        record.save()
        return redirect(self.success_redirect)

class NewOfferView(View):
    """
    Create a new Offer-Record
    """
    template = 'blogs/new_offer.html' # 使用的模板
    success_redirect = 'blogs:all_record' # 成功时重定向地址

    def get(self, request):
        form = Want_form()
        return render(request, self.template,
            context={'form': form})
            
    def post(self, request):
        form = Want_form(request.POST)
        user_id = form.data.get('user_id')
        want = form.data.get('want')
        offer = form.data.get('offer')
        note = form.data.get('note')
        user = SiteUser.objects.get(id = user_id)
        record = Record(is_want=0, want=want, offer=offer, note=note, created_by=user)
        record.save()
        return redirect(self.success_redirect)