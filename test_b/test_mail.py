import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(subject, body, to_email):
    # Set your email and password
    email_address = "your_email@gmail.com"
    email_password = "your_email_password"

    # Set up the MIME
    message = MIMEMultipart()
    message["From"] = email_address
    message["To"] = to_email
    message["Subject"] = subject

    # Attach the body of the email
    message.attach(MIMEText(body, "plain"))

    # Connect to the SMTP server
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        # Start the TLS encryption
        server.starttls()

        # Login to the email account
        server.login(email_address, email_password)

        # Send the email
        server.send_message(message)

if __name__ == "__main__":
    # Example usage
    email_subject = "Test Subject"
    email_body = "This is a test email."
    recipient_email = "recipient@example.com"

    send_email(email_subject, email_body, recipient_email)
