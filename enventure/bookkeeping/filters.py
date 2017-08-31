import django_filters
import models
from rest_framework import viewsets
import rest_framework_filters as filters

class CBODataFilter(filters.FilterSet):
    class Meta:
        model = models.
        fields = {'name': ['exact', 'in', 'startswith']}

class CBOFilter(filters.FilterSet):
    class Meta:
        model = CBO
        fields = {'name': ['exact', 'in', 'startswith']}

class AccountFilter(filters.FilterSet):
    class Meta:
        model = models.Account
        fields = {'name': ['exact', 'in', 'startswith']}



