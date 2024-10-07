document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('.toggle-button').addEventListener('click', function() {
        const reviewForm = document.querySelector('.review-form');
        reviewForm.style.display = reviewForm.style.display === 'none' ? 'block' : 'none';
    });
});
