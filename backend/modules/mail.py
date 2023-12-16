
import os
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(email: str):
    print(email)
    sender = "e.naryshov@gmail.com"
    password = 'walk kafq scgw dkiv'
    receiver = email 
    subject = 'EGOV'
    message =  "Here is your PDF file"
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    
    try:
        server.login(sender, password)
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = receiver
        msg['Subject'] = subject

        body = MIMEText(message)
        msg.attach(body)
        pdf_file_path = '/appp/output.pdf'
        if os.path.exists(pdf_file_path):
            with open(pdf_file_path, 'rb') as pdf_file:
                pdf_attachment = MIMEApplication(pdf_file.read(), _subtype="pdf")
                pdf_file.close()
                pdf_attachment.add_header('Content-Disposition', 'attachment', filename='output.pdf')
                msg.attach(pdf_attachment)
                print(msg)
        else:
            print("PDF file not found at {pdf_file_path}")
        server.sendmail(sender, receiver, msg.as_string())
    except Exception as ex:
        return f"{ex}\nError!"
    finally:
        server.quit()