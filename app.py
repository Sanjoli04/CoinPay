from flask import Flask, request, jsonify, abort, render_template
import razorpay
import os
from dotenv import load_dotenv
import uuid
from supabase import create_client

# --- Setup ---
load_dotenv()
app = Flask(__name__, static_folder='static', template_folder='templates')

# --- Environment Keys ---
# Make sure you have a .env file with these values
SUPABASE_URL = os.getenv("SUPABASE_URL")
ANON_KEY = os.getenv("ANON_KEY")
KEY_ID = os.getenv('KEY_ID')
KEY_SECRET = os.getenv('KEY_SECRET')

# --- Service Clients ---
supabase_client = create_client(SUPABASE_URL, ANON_KEY)
razorpay_client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))

# ======================================================= UTILITY FUNCTIONS ============================
def generate_receipt_id():
    return str(uuid.uuid4())

def insert_row_to_supabase(table_name, row_data):
    try:
        supabase_client.table(table_name).insert(row_data).execute()
    except Exception as e:
        # It's better to handle potential duplicate entries or other DB errors
        print(f"Could not insert row. Maybe user exists? Error: {e}")


def get_all_rows_from_supabase(table_name):
    response = supabase_client.table(table_name).select("*").execute()
    if response.data:
        return response.data
    else:
        raise Exception(f"Error fetching data from {table_name}")

def get_row_by_some_info_from_supabase(table_name, column_name, col_value):
    response = supabase_client.table(table_name).select("*").eq(column_name, col_value).execute()
    if response.data:
        return response.data
    else:
        # This might not be an error if the user is new, so we can return None
        return None

# ======================================================= ERROR HANDLERS ============================
@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Bad Request", "message": str(error.description)}), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not Found", "message": "The requested URL was not found on the server."}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal Server Error", "message": str(error.description)}), 500

# ======================================================= FRONTEND ROUTES =====================================
# These routes will serve your HTML pages
@app.route("/")
def home():
    # Renders the index.html file from the 'templates' folder
    return render_template('index.html')

@app.route("/payment")
def payment_page():
    # Renders the payment.html file from the 'templates' folder
    return render_template('payment.html')

# ======================================================= API ROUTES =====================================
@app.route("/create-order", methods=["POST"])
def create_order():
    data = request.get_json()
    required_keys = ["amount", "fullname", "email", "phone"]
    if not all(key in data for key in required_keys):
        abort(400, description="Missing required fields to create an order.")
    
    amount = data.get("amount") * 100  # Convert to paise
    currency = "INR"
    receipt = generate_receipt_id()

    order_options = {
        "amount": amount,
        "currency": currency,
        "receipt": receipt,
        "payment_capture": 1
    }
    
    try:
        order = razorpay_client.order.create(order_options)
        
        user = {
            "fullname": data.get("fullname"),
            "email": data.get("email"),
            "phone": data.get("phone"),
        }
        insert_row_to_supabase("users", user)

        # IMPORTANT: We send the Key ID to the frontend here
        # This is more secure than hardcoding it in your JavaScript
        return jsonify({
            "order": order,
            "razorpay_key_id": KEY_ID 
        }), 200

    except Exception as e:
        abort(500, description=str(e))


@app.route("/verify-payment-signature", methods=["POST"])
def verify_payment_signature():
    data = request.get_json()
    try:
        # This utility function will raise an exception if the signature is not valid
        razorpay_client.utility.verify_payment_signature(data)
        
        # If verification is successful, you can update your database here
        # For example, mark the order as paid.
        
        return jsonify({"status": "success", "message": "Payment signature verified successfully"})
    except Exception as e:
        abort(400, description=str(e))


@app.route("/methods", methods=["GET"])
def get_payment_methods():
    try:
        payment_methods = get_all_rows_from_supabase("payment_methods")
        return jsonify(payment_methods), 200
    except Exception as e:
        abort(500, description=str(e))

# --- Main Execution ---
if __name__ == '__main__':
    # debug=True is great for development, shows detailed errors
    app.run(debug=True)
