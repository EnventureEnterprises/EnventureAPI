from django import forms
from .models import Notification
import models



class NotificationForm(forms.ModelForm):
    class Meta:
        model = models.Notification
        fields = ['message','title','uri','dialogYes','dialogNo' ]

class EntryForm(forms.ModelForm):
    account = forms.ModelChoiceField(
        queryset=models.Account.objects, required=False, widget=forms.HiddenInput()
    )

    amount = forms.DecimalField(
        required=False,
        max_digits=16,
        decimal_places=2,
        widget=forms.HiddenInput())

    target = forms.ChoiceField(label='account and lot')
    is_credit = forms.ChoiceField()


    
    
    