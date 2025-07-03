import re
import dns.resolver
import smtplib
import socket

def is_valid_format(email):
    """Check email format with regex."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def get_mx_record(domain):
    """Get MX record for the domain."""
    try:
        answers = dns.resolver.resolve(domain, 'MX')
# answers will have return object as follow 
#     answers = [
#     MX(preference=30, exchange='alt3.gmail-smtp-in.l.google.com.'),
#     MX(preference=10, exchange='alt1.gmail-smtp-in.l.google.com.'),
#     MX(preference=5,  exchange='gmail-smtp-in.l.google.com.'),
#     MX(preference=20, exchange='alt2.gmail-smtp-in.l.google.com.')
#    ]
        return str(sorted(answers, key=lambda x: x.preference)[0].exchange)
# SORt array and take with lowest preference first
# as lowest preference is the primary MX server  and with highest priority
# e.g. gmail-smtp-in.l.google.com. is the primary MX server for gmail
#     [
#     MX(preference=5,  exchange='gmail-smtp-in.l.google.com.'),
#     MX(preference=10, exchange='alt1.gmail-smtp-in.l.google.com.'),
#     MX(preference=20, exchange='alt2.gmail-smtp-in.l.google.com.'),
#     MX(preference=30, exchange='alt3.gmail-smtp-in.l.google.com.')
# ]


    except Exception as e:
        print(f"[MX ERROR] {e}")
        return None

def smtp_check(email, mx_host):
    """Try SMTP connection to check recipient validity."""
    try:
        # Create a client Object for the SMTP Handshake with a timeout
        server = smtplib.SMTP(timeout=10)
        server.connect(mx_host) # host is like google mail server or other e.g gmail-smtp-in.l.google.com
        
        server.helo('adityaiscool.com')  # it is sending helo request to out host  this domain has not be real give any other fake domain  e.g. example.com

        # Similarly simulate send mail from command
        server.mail('test@example.com') 
        
        code, message = server.rcpt(email)  # RCPT TO
        server.quit()
        return code == 250  # 250 OK means accepted
        # for False SMTP server will return 550 or 554 depeinding on the mx_host
        
    except (socket.timeout, smtplib.SMTPServerDisconnected, smtplib.SMTPConnectError) as e:
        print(f"[SMTP ERROR] {e}")
        return False

def validate_email(email):
    if not is_valid_format(email):
        return False, "Invalid email format"

    domain = email.split('@')[-1]
    mx_host = get_mx_record(domain)
    if not mx_host:
        return False, "No MX record for domain"

    is_valid = smtp_check(email, mx_host)
    if not is_valid:
        return False, "SMTP rejected recipient"
    
    return True, "Email is likely valid"

if __name__ == "__main__":
    test_email = input("Enter email to verify: ").strip()
    result, reason = validate_email(test_email)
    print(f"Result: {'✅ Valid Email' if result else '❌ Invalid'} | Reason: {reason}")