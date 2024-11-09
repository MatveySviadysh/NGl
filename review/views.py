from django.shortcuts import redirect, render
from review.forms import CommentForm
from user.models import Tutor
from review.models import Comment
from django.core.paginator import Paginator

def add_comment(request, tutor_id):
    tutor = Tutor.objects.get(id=tutor_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.tutor = tutor
            comment.user = request.user
            comment.save()
            return redirect('profile-tutor', full_name=tutor.full_name)
    else:
        form = CommentForm()
    return render(request, 'review/add_comment.html', {
        'form': form,
        'tutor': tutor
    })

def ALLReviewTutor(request):
    all_reviews = Comment.objects.all()
    paginator = Paginator(all_reviews, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'review/ALLReviewTutor.html',{'all_reviews':all_reviews ,'page_obj': page_obj})