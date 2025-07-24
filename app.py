from flask import Flask, request, jsonify, abort
import razorpay
import os
from dotenv import load_dotenv
import uuid
from supabase import create_client
load_dotenv()
app = Flask(__name__)
supabase_client = create_client(os.getenv("SUPABASE_URL"), os.getenv("ANON_KEY"))
KEY_ID = os.getenv('KEY_ID')
KEY_SECRET = os.getenv('KEY_SECRET')
razorpay_client = razorpay.Client(auth=(KEY_ID,KEY_SECRET))
# ======================================================= UTILITY FUNCTIONS ============================
def generate_receipt_id():
    return str(uuid.uuid4())
def insert_row_to_supabase(table_name,row_data):
    supabase_client.table(table_name).insert(row_data).execute()
def get_all_rows_from_supabase(table_name):
    response = supabase_client.table(table_name).select("*").execute()
    if response.data:
        return response.data
    else:
        raise Exception(f"Error fetching data from {table_name}: {response.error}")
def get_row_by_some_info_from_supabase(table_name, column_name, col_value):
    response = supabase_client.table(table_name).select("*").eq(column_name, col_value).execute()
    if response.data:
        return response.data
    else:
        raise Exception(f"Error fetching data from {table_name} where {column_name} = {col_value}: {response.error}")
# ======================================================= ERROR HANDLERS ============================
@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Bad Request", "message": str(error)}), 400
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": str(error)}),404
@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": str(error)}),500
# ======================================================= ROUTES =====================================

@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Razorpay Payment API"}), 200
@app.route("/create-order",methods=["POST"])
def create_order():
    data = request.get_json()
    if not "amount" in data.keys():
        abort(400, description="Amount is required to create an order")
    
    amount = data.get("amount") * 100
    currency = "INR"
    receipt = generate_receipt_id()

    order = razorpay_client.order.create(
        {
            "amount": amount,
            "currency": currency,
            "receipt": receipt,
            "payment_capture": 1
        }
    )
    user = {
        "fullname": data.get("fullname"),
        "email": data.get("email"),
        "phone": data.get("phone"),
    }
    insert_row_to_supabase("users", user)
    user_info = get_row_by_some_info_from_supabase("users", "email", user["email"])[0]
    return jsonify({
        "order": order,
        "user_id" : user_info.get("id"),
    }),200

@app.route("/verify-payment-signature", methods=["POST"])
def verify_payment_signature():
    data = request.get_json()
    try:
        razorpay_client.utility.verify_payment_signature(data)
        return jsonify({"status": "success", "message": "Payment signature verified successfully"})
    except Exception as e:
        abort(500, description = e)
@app.route("/methods", methods=["GET"])
def get_payment_methods():
    try:
        payment_methods = get_all_rows_from_supabase("payment_methods")
        return jsonify(payment_methods),200
    except Exception as e:
        abort(500, description=str(e))

app.run(debug=True)