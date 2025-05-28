import smtplib
import pandas as pd 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
from datetime import datetime 
import logging

logging.basicConfig(filename='notifications.log',
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()

def user_table():
    """
    Creates a table that contains user informations    

    """
    users = pd.DataFrame({
        'user_id': [101, 102],
        'name': ['Rafiu Abowaba', 'Taibat Abowaba'],
        'email': ['Abowabaolamide@gmail.com', 'abowabataibat@gmail.com'] 
    })
    return users

def transaction_table():
    """
      Creates a table that contains debit and credit transactions 
    """
    transactions = pd.DataFrame({
        'transaction_id': [1, 2],
        'user_id': [102, 101],
        'amount': [55000, 100000], 
        'transaction_type': ['credit', 'debit'],
        'balance': [2000000, 300000],
        'remark': ['fuel', 'groceries'],
        'date_time': [datetime.now().strftime("%Y-%m-%d %H:%M:%S"), datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
    })
    return transactions

def login_table():
    """
    Creates a table that contains log in informations   
    """
    logins = pd.DataFrame({
        'login_id': [1],
        'user_id': [102],
        'date_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    return logins


def send_mail():
    """
       Sends transaction notification emails to users.

      - Merges the transaction table with the user table to retrieve user details like email.
      - Connects to the Gmail SMTP server, encrypts the connection using TLS, and logs in the client.
      - If login data exists, it loops through each record and sends an email with both plain text and HTML versions using MIMEMultipart.
      - If no data is found, logs an informational message.
      - Logs an error if email sending fails due to an exception.

    """
    transaction_data = transaction_table().merge(user_table(), on = 'user_id')
    host = 'smtp.gmail.com'
    port = 587
    sender_email = "abowabat@gmail.com"
    sender_password = os.getenv('password')
    subject = "Transaction Notification"
    try:
        server = smtplib.SMTP(host, port)
        server.starttls()

        server.login(sender_email, sender_password)

        if not transaction_data.empty:
            for _, row in transaction_data.iterrows():
                msg = MIMEMultipart('alternative')
                msg['From'] = sender_email
                msg['To'] = row['email']
                msg['Subject'] = subject 
                text = f""" Dear {row['name']}
                                Guaranty Trust Bank electronic Notification Service (GeNS)
                                We wish to inform you that a {row['transaction_type']} transaction occurred on your account.

                                Description: Electronic Money Transfer Levy - {row['date_time']}
                                Amount: NGN {row['amount']}
                                Remarks: {row['remark']}
                                Time of Transaction: {row['date_time']}
                                Document Number: 
                                Available Balance: NGN {row['balance']}

                                The privacy and security of your Bank Account details is important to us. 
                                If you would prefer that we do not display your account balance in every transaction alert sent to you via email, 
                                please dial *737*51*1#.

                                Thank you for choosing Guaranty Trust Bank Limited.
                                """
                html = f"""<html>
                        <body>
                        <p> Dear <strong>{row['name']}</strong></p>
                                    <p> Guaranty Trust Bank electronic Notification Service (GeNS) </p>
                                    <p>We wish to inform you that a {row['transaction_type']} transaction occurred on your account.</p>
                                    <p><strong>Description:</strong> Electronic Money Transfer Levy - {row['date_time']}<br>
                                    <strong>Amount:</strong> NGN {row['amount']}<br>
                                    <strong>Remarks:</strong> {row['remark']}<br>
                                    <strong>Time of Transaction:</strong> {row['date_time']}<br>
                                    <strong>Document Number:</strong><br>
                                    <strong>Available Balance:</strong> NGN {row['balance']}</p>                                    
                                    <p>The privacy and security of your Bank Account details is important to us. 
                                    If you would prefer that we do not display your account balance in every transaction alert sent to you via email, 
                                    please dial *737*51*1#.</p>
                                    
                                    <p>Thank you for choosing Guaranty Trust Bank Limited.</p></body></html>"""
                text_message = MIMEText(text, 'plain')
                html_message = MIMEText(html, 'html')
                msg.attach(text_message)
                msg.attach(html_message)

                server.sendmail(sender_email, row['email'], msg.as_string())

                logging.info(f'Transaction email sent succesfully to {row['name']}')
            server.quit()
        else:
            logging.info('No transactions found.')
    except smtplib.SMTPException as e:
            logging.error(f'Error sending email: {e}')


def login_notifications():
    """
       Sends login notification emails to users.

      - Merges the login table with the user table to retrieve user details like email.
      - Connects to the Gmail SMTP server, encrypts the connection using TLS, and logs in the client.
      - If login data exists, it loops through each record and sends an email with both plain text and HTML versions using MIMEMultipart.
      - If no data is found, logs an informational message.
      - Logs an error if email sending fails due to an exception. 
    """
    login_info = login_table().merge(user_table(), on = 'user_id')
    host = 'smtp.gmail.com'
    port = 587
    sender_email = "abowabat@gmail.com"
    sender_password = os.getenv('password')
    subject = "GTWorld Notification"
    try: 
        server = smtplib.SMTP(host, port)
        server.starttls()

        server.login(sender_email, sender_password)
        if not login_info.empty:
            for _, row in login_info.iterrows():
                msg = MIMEMultipart('alternative')
                msg['From'] = sender_email
                msg['To'] = row['email']
                msg['Subject'] = subject
                text = f""" Dear {row['name']},

                                    GTWORLD LOG IN CONFIRMATION

                                    Please be informed that your mobile banking profile was accessed at {row['date_time']}
                            """
                html = f"""<html>
                    <body>
                    Dear <strong>{row['name']}, </strong>
                                        <p><strong>GTWORLD LOG IN CONFIRMATION</strong></p>
                                        <p> Please be informed that your mobile banking profile was accessed at {row['date_time']}. </p></body></html>"""
                text_message = MIMEText(text, 'plain')
                html_message = MIMEText(html, 'html')
                msg.attach(text_message)
                msg.attach(html_message)
        

                server.sendmail(sender_email, row['email'], msg.as_string())

                logging.info(f'Login email sent succesfully to: {row['name']}')

            server.quit()
        else:
            logging.info('No logins found')

    except smtplib.SMTPException as e:
            logging.error(f'Error sending email {e}')
    


send_mail()
login_notifications()


