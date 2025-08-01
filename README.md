# 📧 Email Validator – Python (Format + MX + SMTP)

This is a simple Python script to validate whether an email address is **likely real**, by checking:

1. ✅ Proper format (regex)
2. 📡 MX (Mail Exchange) DNS record
3. 📬 Mailbox existence via SMTP handshake

## 🚀 How It Works

### ✅ Step 1: Format Validation
Checks the structure of the email using a regular expression.

### 📡 Step 2: MX Record Check
Uses DNS to get the domain’s MX records. If no MX exists, the domain can't receive email.

### 📬 Step 3: SMTP Check
Connects to the domain’s primary mail server and simulates sending a message (no real email is sent). If the server responds with code `250`, the recipient likely exists.


## 🔧 Dependancy Requirements : 
- Python 3.6+
- dnspython
- requests
- python_dotenv

## 📦 Steps :
### 1. Create a VENV first 
```sh
python -m venv venv
```

### 2. Activate VENV 
```sh
./venv/Scripts/activate
```

### 3. Download All Requirements 
```sh
pip install -r requirements.txt
```

## Flow Diagram : 
![diagram-export-03-07-2025-06_45_04](https://github.com/user-attachments/assets/b33e7b1a-8d1d-4637-b0cc-eeab3f39a313)
Github Repo For Finding All Disposable Emails across Web : https://raw.githubusercontent.com/disposable/disposable-email-domains/master/domains.txt

## Results : 
### For EMAIL verifier API check [Hunter.io](https://hunter.io/) .


### Without API :
<img width="379" alt="image" src="https://github.com/user-attachments/assets/abd7909d-8a58-4e35-a118-9ba31a9dc2e5" />

### With API : 
![Screenshot 2025-07-03 065519](https://github.com/user-attachments/assets/69eb6f19-d48b-4d1d-9ce4-b35618d366ff)
