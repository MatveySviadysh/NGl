document.addEventListener('DOMContentLoaded', function() {
    const toggleButton = document.querySelector('.toggle-button');
    const reviewForm = document.querySelector('.review-form');

    if (toggleButton) {
        toggleButton.addEventListener('click', function(e) {
            e.preventDefault(); // Prevent default anchor click behavior
            
            // Toggle visibility of the review form
            if (reviewForm.style.display === 'none' || reviewForm.style.display === '') {
                reviewForm.style.display = 'block'; // Show the form
                reviewForm.style.opacity = 1; // Ensure opacity is set to 1
                reviewForm.scrollIntoView({
                    behavior: 'smooth', // Smooth scroll
                    block: 'start' // Align to the top of the viewport
                });
            } else {
                reviewForm.style.opacity = 0; // Fade out
                setTimeout(() => { 
                    reviewForm.style.display = 'none'; // Hide after fade out
                }, 500); // Match this duration with CSS transition time
            }
        });
    }

    // Smooth scrolling for other anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault(); // Prevent default anchor click behavior
            const targetId = this.getAttribute('href'); // Get the target ID
            const targetElement = document.querySelector(targetId); // Find the target element
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth', // Smooth scroll
                    block: 'start' // Align to the top of the viewport
                });
            }
        });
    });
});
