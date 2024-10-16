from django.shortcuts import redirect, render, get_object_or_404
from .models import ChatRoom, Message

def chat_with_tutor(request, chatroom_id):
    chatroom = get_object_or_404(ChatRoom, id=chatroom_id)
    messages = chatroom.messages.all()

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            message = Message.objects.create(
                sender=request.user,
                recipient=chatroom.responder if request.user == chatroom.requester else chatroom.requester,
                chatroom=chatroom,
                content=content,
            )
            message.save()
    return render(request, 'chat/pages/Chat.html', {
        'chatroom': chatroom,
        'messages': messages,
    })

def tutor_chat_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    chatrooms = ChatRoom.objects.filter(responder=request.user)
    return render(request, 'chat/pages/TutorChatList.html', {
        'chatrooms': chatrooms,
    })