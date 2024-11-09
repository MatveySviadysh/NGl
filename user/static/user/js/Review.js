document.addEventListener('DOMContentLoaded', function() {
    const toggleButton = document.querySelector('.toggle-button');
    const reviewForm = document.querySelector('.review-form');

    if (toggleButton) {
        toggleButton.addEventListener('click', function(e) {
            e.preventDefault();
            
            if (reviewForm.style.display === 'none' || reviewForm.style.display === '') {
                reviewForm.style.display = 'block';
                reviewForm.style.opacity = 1;
                reviewForm.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            } else {
                reviewForm.style.opacity = 0;
                setTimeout(() => { 
                    reviewForm.style.display = 'none';
                }, 500);
            }
        });
    }

    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});
