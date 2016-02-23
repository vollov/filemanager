from django.shortcuts import render

from django.http import HttpResponseForbidden

def forbiddenView(request):
  raise HttpResponseForbidden()
