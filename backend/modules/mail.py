
import os
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(email:str):
    sender = "e.naryshov@gmail.com"
    password = ''
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

        pdf_directory = r'/appp/output.pdf'
        for filename in os.listdir(pdf_directory):
            if filename.endswith('.pdf'):
                with open(os.path.join(pdf_directory, filename), 'rb') as pdf_file:
                    pdf_attachment = MIMEApplication(pdf_file.read(), _subtype="pdf")
                    pdf_file.close()
                    pdf_attachment.add_header('Content-Disposition', 'attachment', filename=filename)
                    msg.attach(pdf_attachment)

        server.sendmail(sender, receiver, msg.as_string())
        return 'The message was sent successfully!'
    except Exception as ex:
        return f"{ex}\nError!"
    finally:
        server.quit()