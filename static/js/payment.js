document.addEventListener('DOMContentLoaded', function() {
    const storedDetails = localStorage.getItem('paymentDetails');
    if (!storedDetails) {
        window.location.href = '/';
        return;
    }

    const paymentDetails = JSON.parse(storedDetails);

    // Populate Left Panel UI
    document.getElementById('orderId').textContent = `Order #${paymentDetails.razorpay_order_id}`;
    document.getElementById('paymentAmount').textContent = `₹${Number(paymentDetails.amount).toLocaleString('en-IN')}`;
    
    // Populate Right Panel Order Summary
    document.getElementById('summaryName').textContent = paymentDetails.fullname;
    // CORRECTED: Changed "a.email" to "paymentDetails.email"
    document.getElementById('summaryEmail').textContent = paymentDetails.email;
    document.getElementById('summaryMobile').textContent = paymentDetails.phone;
    document.getElementById('summaryAmount').textContent = `₹${Number(paymentDetails.amount).toLocaleString('en-IN')}`;


    // Razorpay Payment Initialization
    const payNowBtn = document.getElementById('payNowBtn');
    payNowBtn.addEventListener('click', function() {
        const options = {
            key: paymentDetails.razorpay_key_id,
            amount: paymentDetails.amount * 100,
            currency: "INR",
            name: "CampusX",
            description: `Payment for Order #${paymentDetails.razorpay_order_id}`,
            order_id: paymentDetails.razorpay_order_id,
            
            handler: async function (response) {
                const data = {
                    razorpay_payment_id: response.razorpay_payment_id,
                    razorpay_order_id: response.razorpay_order_id,
                    razorpay_signature: response.razorpay_signature
                };

                try {
                    const verificationResponse = await fetch('/verify-payment-signature', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(data)
                    });

                    if (!verificationResponse.ok) throw new Error('Payment verification failed.');
                    
                    const result = await verificationResponse.json();
                    alert(`Payment Successful! Status: ${result.status}`);
                    localStorage.removeItem('paymentDetails');
                    window.location.href = '/';

                } catch (error) {
                    console.error('Verification error:', error);
                    alert(`Payment verification failed: ${error.message}`);
                }
            },
            prefill: {
                name: paymentDetails.fullname,
                email: paymentDetails.email,
                contact: paymentDetails.phone
            },
            theme: {
                color: "#4f46e5"
            }
        };
        const rzp = new Razorpay(options);
        
        rzp.on('payment.failed', function (response){
            alert(`Payment Failed: ${response.error.description}`);
            console.error(response.error);
        });

        rzp.open();
    });
});
