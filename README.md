# 📧 Email Validator – Python (Format + MX + SMTP)

This is a simple Python script to validate whether an email address is **likely real**, by checking:

1. ✅ Proper format (regex)
2. 📡 MX (Mail Exchange) DNS record
3. 📬 Mailbox existence via SMTP handshake


---

## 🚀 How It Works

### ✅ Step 1: Format Validation
Checks the structure of the email using a regular expression.

### 📡 Step 2: MX Record Check
Uses DNS to get the domain’s MX records. If no MX exists, the domain can't receive email.

### 📬 Step 3: SMTP Check
Connects to the domain’s primary mail server and simulates sending a message (no real email is sent). If the server responds with code `250`, the recipient likely exists.

---

## 🔧 Requirements

- Python 3.6+
- `dnspython` module
- requests
- python_dotenv

### 📦 Install

```bash
pip install dnspython

----
Architecture and Flow Diagram 



