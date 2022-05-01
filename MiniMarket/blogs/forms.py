from django import forms
from django.forms import fields, ModelForm
from django.core.exceptions import ValidationError

from .models import *

class Want_form(ModelForm):
    class Meta:
        model = Record
        fields = ['want', 'offer', 'note', 'created_by']
        help_texts = {
            'want': '你想要啥？',
            'offer': '你能提供什么？',
            'note': '备注',
        }

    def save(self, commit=True):
        record = super().save(commit=False)
        record.is_want = True
        if commit:
            record.save()
        return record


class Offer_form(ModelForm):
    class Meta:
        model = Record
        fields = ['offer', 'want', 'note', 'created_by']
        help_texts = {
            'want': '你想要啥？',
            'offer': '你能提供什么？',
            'note': '备注',
        }

    def save(self, commit=True):
        record = super().save(commit=False)
        record.is_want = False
        if commit:
            record.save()
        return record