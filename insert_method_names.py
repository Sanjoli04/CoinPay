from supabase import create_client
import os
from dotenv import load_dotenv
load_dotenv()
supabase_client = create_client(os.getenv("SUPABASE_URL"), os.getenv("ANON_KEY"))
 
payment_methods = [
    {"method_name": "UPI", "enabled": True},
    {"method_name": "Card", "enabled": True},
    {"method_name": "Net Banking", "enabled": True},
    {"method_name": "Wallets", "enabled": True},
    {"method_name": "EMI", "enabled": True},
    {"method_name": "Cardless EMI", "enabled": True},
    {"method_name": "Pay Later", "enabled": True}
]

for method_obj in payment_methods:
    supabase_client.table("payment_methods").insert(method_obj).execute()