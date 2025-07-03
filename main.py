import re
import dns.resolver
import smtplib
import socket
import tldextract
import requests

# Initialize TLD Extractor
extractor = tldextract.TLDExtract()

# Global set to cache disposable domains
disposable_domains_set = set()

def load_disposable_domains():
    """Fetch disposable email domains from GitHub and load into a set."""
    global disposable_domains_set
    try:
        url = "https://raw.githubusercontent.com/disposable/disposable-email-domains/master/domains.txt"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            lines = response.text.splitlines()
            disposable_domains_set = {line.strip().lower() for line in lines if line.strip() and not line.startswith("#")}
        else:
            print("[ERROR] Failed to fetch disposable domains list.")
    except Exception as e:
        print(f"[ERROR] Could not load disposable domain list: {e}")

def is_valid_format(email):
    """Check email format with regex."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def is_disposable_email(email):
    """Check if email is from a known disposable domain."""
    domain = email.split('@')[-1].lower()
    ext = extractor(domain)
    base_domain = f"{ext.domain}.{ext.suffix}" if ext.domain and ext.suffix else domain
    return base_domain in disposable_domains_set

def get_mx_record(domain):
    """Get MX record for the domain."""
    try:
        answers = dns.resolver.resolve(domain, 'MX')
        return str(sorted(answers, key=lambda x: x.preference)[0].exchange).rstrip('.')
    except Exception as e:
        print(f"[MX ERROR] {e}")
        return None

def smtp_check(email, mx_host):
    """Try SMTP connection to check recipient validity."""
    try:
        server = smtplib.SMTP(timeout=10)
        server.connect(mx_host)
        server.helo('example.com')  # fake domain is fine
        server.mail('test@example.com') 
        code, message = server.rcpt(email)
        server.quit()
        return code == 250
    except (socket.timeout, smtplib.SMTPServerDisconnected, smtplib.SMTPConnectError) as e:
        print(f"[SMTP ERROR] {e}")
        return False

def validate_email(email):
    """Full email validation pipeline."""
    if not is_valid_format(email):
        return False, "Invalid email format"

    if is_disposable_email(email):
        return False, "Disposable email detected – skipping further validation"

    domain = email.split('@')[-1]
    mx_host = get_mx_record(domain)
    if not mx_host:
        return False, "No MX record for domain"

    is_valid = smtp_check(email, mx_host)
    if not is_valid:
        return False, "SMTP rejected recipient"
    
    return True, "Email is likely valid"

if __name__ == "__main__":
    load_disposable_domains()
    test_email = input("Enter email to verify: ").strip()
    result, reason = validate_email(test_email)
    print(f"Result: {'✅ Valid Email' if result else '❌ Invalid'} | Reason: {reason}")