from cgitb import lookup
from socket import fromshare
from tkinter.ttk import Widget
import django_filters
from django import forms
from . import models


class ProductFilter(django_filters.FilterSet):
    brand=django_filters.ModelMultipleChoiceFilter(queryset=models.Brand.objects.all(),widget=forms.CheckboxSelectMultiple)