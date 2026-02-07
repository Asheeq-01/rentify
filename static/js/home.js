
document.addEventListener('DOMContentLoaded', function () {

    const filterBtns = document.querySelectorAll('.filter-btn');
    const vehicleItems = document.querySelectorAll('.vehicle-item');
    const searchInput = document.getElementById('vehicleSearch');
    const categorySelect = document.getElementById('categoryFilter');

    // Button filter
    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            filterVehicles();
        });
    });





    // Search & dropdown
    if (searchInput) searchInput.addEventListener('input', filterVehicles);
    if (categorySelect) categorySelect.addEventListener('change', filterVehicles);

    function filterVehicles() {
        const activeBtn = document.querySelector('.filter-btn.active');
        const activeFilter = activeBtn ? activeBtn.dataset.filter : 'all';
        const searchTerm = searchInput ? searchInput.value.toLowerCase() : '';
        const activeCategory = categorySelect ? categorySelect.value : 'all';

        vehicleItems.forEach(item => {
            const category = item.dataset.category; // CAR / BIKE / VAN
            const name = item.dataset.name;         // lowercase name

            const matchesFilter =
                activeFilter === 'all' || category === activeFilter;

            const matchesCategory =
                activeCategory === 'all' || category === activeCategory;

            const matchesSearch =
                name.includes(searchTerm);

            if (matchesFilter && matchesCategory && matchesSearch) {
                item.style.display = 'block';
                item.style.animation = 'fadeIn 0.4s ease forwards';
            } else {
                item.style.display = 'none';
            }
        });
    }
});

