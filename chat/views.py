from django.shortcuts import render

def chat_with_tutor(request):
    return render(request, 'chat/pages/Chat.html')