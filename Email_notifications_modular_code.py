import pandas as pd 
import os 
import time 
import smtplib
import logging
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart 


def send_mail(port: int, host: str, sender_email: str, sender_password: str, table: pd.DataFrame, subject: str, text: str, html) -> None:
    """ 
    Sends email using smtplib to a list of reciepients 
       Args:
          port (int): The SMTP port used by the email provider
          host (str): The SMTP server address 
          sender_email (str): The sender's email address
          sender_password (str): The sender's email app password.
          table (pd.DataFrame): A DataFrame containing a list of reciepients
          subject (str): The subject line of the email
          text (str): The plain text version of the email body
          html: The HTML version of the email body

       Returns:
          None
    """
    try:
        if not table.empty:
            for _, row in table.iterrows():
                msg = MIMEMultipart('alternative')
                msg['From'] = sender_email
                msg['To'] = row['email']
                msg['Subject'] = subject
                text_msg = text.format(**row.to_dict())
                html_msg = html.format(**row.to_dict())
                text_message = MIMEText(text_msg, 'plain')
                html_message = MIMEText(html_msg, 'html')
                msg.attach(text_message)
                msg.attach(html_message)

                with smtplib.SMTP(host, port) as server:
                    server.starttls()
                    server.login(sender_email, sender_password)
                    server.sendmail(sender_email, row['email'], msg.as_string())
                    logging.info(f"Email sent to {row['name']} successfully")
        else:
            logging.info('No record found')
    except Exception as e:
        logging.error(f'Error sending emails: {e}')



    
