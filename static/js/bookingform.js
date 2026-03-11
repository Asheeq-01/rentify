document.addEventListener('DOMContentLoaded', function () {

    const form = document.getElementById('bookingForm');
    const dailyPrice = form.dataset.price;

    const startInput = document.getElementById('start_date');
    const endInput = document.getElementById('end_date');

    function updatePrice() {

        if (startInput.value && endInput.value) {

            const s = new Date(startInput.value);
            const e = new Date(endInput.value);

            const days = Math.ceil((e - s) / (1000 * 60 * 60 * 24));

            if (days > 0) {

                const total = days * dailyPrice;

                document.getElementById('daysCount').innerText = days;
                document.getElementById('subtotal').innerText = total.toLocaleString('en-IN');
                document.getElementById('totalAmount').innerText = total.toLocaleString('en-IN');

            }

        }

    }

    startInput.addEventListener('change', () => {
        endInput.min = startInput.value;
        updatePrice();
    });

    endInput.addEventListener('change', updatePrice);

});