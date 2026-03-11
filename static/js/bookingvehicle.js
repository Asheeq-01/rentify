document.addEventListener('DOMContentLoaded', function() {

    const carousel = document.getElementById('vehicleCarousel');
    const counter = document.querySelector('.image-counter');

    if (carousel && counter) {

        // Count total images
        const totalItems = document.querySelectorAll('#vehicleCarousel .carousel-item').length;

        // Set default counter on page load
        counter.textContent = `1 / ${totalItems}`;

        // Update counter when sliding
        carousel.addEventListener('slid.bs.carousel', function(event) {

            const activeIndex = event.to;

            counter.textContent = `${activeIndex + 1} / ${totalItems}`;

        });
    }

});