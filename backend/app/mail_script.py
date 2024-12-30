import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(to_email, subject, body):
    sender_email = "example@gmail.com" # Sender's email credentials
    sender_password = "xxxx yyyy aaaa zzzz"  # Use an app-specific password if using Gmail

    # Create the email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Attach the email body
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to the SMTP server
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Upgrade to secure connection
            server.login(sender_email, sender_password)  # Log in to the server
            server.send_message(msg)  # Send the email
        print(f"Email sent successfully to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Example usage
def generate_link(email, token, host):
    recipient_email = email
    email_subject = "Password Reset Link"
    reset_link = f"http://{host}/reset-password.html?token={token}"
    email_body = f"Click the link to reset your password: {reset_link}"

    send_email(recipient_email, email_subject, email_body)

    return {"success": True, "message": "Reset link sent"}, 200