document.addEventListener('DOMContentLoaded', function() {
    const userDetailsForm = document.getElementById('userDetailsForm');
    const submitBtn = document.getElementById('submitBtn');
    const btnText = submitBtn.querySelector('.btn-text');
    const spinner = submitBtn.querySelector('.spinner-icon');
    const formError = document.getElementById('formError');

    userDetailsForm.addEventListener('submit', async function(event) {
        event.preventDefault();
        formError.textContent = '';

        if (!userDetailsForm.checkValidity()) {
            formError.textContent = 'Please fill out all fields correctly.';
            return;
        }

        btnText.classList.add('hidden');
        spinner.classList.remove('hidden');
        submitBtn.disabled = true;

        const formData = new FormData(userDetailsForm);
        const userData = {
            fullname: formData.get('fullname'),
            email: formData.get('email'),
            phone: formData.get('phone'),
            amount: Number(formData.get('amount')) 
        };

        try {
            const response = await fetch('/create-order', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(userData),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || 'Failed to create order.');
            }

            const responseData = await response.json();
            
            const paymentDetails = {
                ...userData,
                razorpay_order_id: responseData.order.id,
                razorpay_key_id: responseData.razorpay_key_id 
            };

            localStorage.setItem('paymentDetails', JSON.stringify(paymentDetails));

            // CORRECTED: Redirect to the /payment route handled by Flask
            window.location.href = '/payment';

        } catch (error) {
            console.error('Error creating order:', error);
            formError.textContent = `Error: ${error.message}`;
            btnText.classList.remove('hidden');
            spinner.classList.add('hidden');
            submitBtn.disabled = false;
        }
    });
});
