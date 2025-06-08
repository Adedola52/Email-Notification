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
        # connects to the SMTP server and login
        with smtplib.SMTP(host, port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            if not table.empty:
                # iterates the DataFrame to send emails to each receipients
                for _, row in table.iterrows():
                    try:
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

                        # sends email to each reciepients 
                        server.sendmail(sender_email, row['email'], msg.as_string())
                        logging.info(f"{subject} Email sent to {row['name']} successfully")

                    # raises an exception when sending to a receipient fails    
                    except Exception as e:
                        logging.info(f"Error sending emails to {e}")

            # returns an else statement when there is no record found 
            else:
                logging.info('No record found')

    # raises an exception when a connection error occurs             
    except smtplib.SMTPException as e:
        logging.error(f'Error with {e}')



    
