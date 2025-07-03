import requests
from dotenv import load_dotenv
import os
load_dotenv()

# Access the Env file
HUNTER_IO_API_KEY = os.getenv("HUNTER_IO_API_KEY")  

# Email Input
email="adityaisamkad1234@gmail.com"

def hunter_io_email_verification(email):
    url = "https://api.hunter.io/v2/email-verifier"
    params = {
        "email": email,
        "api_key": HUNTER_IO_API_KEY
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
        
        if data.get("data"):
            verification_data = data["data"]
            print(f"Email: {verification_data['email']}")
            print(f"Email Status: {verification_data['status']}")
            print(f"Result: {verification_data['result']}")
            print(f"Score: {verification_data['score']}")
            print(f"Email Format Check: {verification_data['regexp']}")
            print(f"Disposable: {verification_data['disposable']}")
            print(f"Webmail: {verification_data['webmail']}")
            print(f"MX Records: {verification_data['mx_records']}")
            print(f"SMTP_HANDSHAKE: {verification_data['smtp_server']}")
            print(f"SMTP_CHECK: {verification_data['smtp_check']}")
        else:
            print("No data found for the provided email.")
    
    except requests.RequestException as e:
        print(f"Error fetching data from Hunter.io: {e}")


if __name__=="__main__":
    hunter_io_email_verification(email)