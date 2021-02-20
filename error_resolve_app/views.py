from django.shortcuts import render, redirect
from django.views import View
# Create your views here.

class HomeView(View):

    def get(self, request, *args, **kwargs):

        return render(request, 'error_resolve_app/home.html')
