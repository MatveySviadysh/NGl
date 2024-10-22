from django.shortcuts import redirect, render
from review.forms import CommentForm
from user.models import Tutor

def add_comment(request, tutor_id):

    tutor = Tutor.objects.get(id=tutor_id)

    

    if request.method == 'POST':

        form = CommentForm(request.POST)

        if form.is_valid():

            comment = form.save(commit=False)

            comment.tutor = tutor

            comment.user = request.user

            comment.save()

            # Redirect to the profile page without changing it

            return redirect('profile-tutor', full_name=tutor.full_name)

    else:

        form = CommentForm()

    

    return render(request, 'review/add_comment.html', {

        'form': form,

        'tutor': tutor

    })
