from django.views import View
from django.shortcuts import render


class ButtonPageView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'mybot/button.html')
