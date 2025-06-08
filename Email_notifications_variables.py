import pandas as pd 
import os 
import time 
import smtplib
import logging
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from Email_notifications_modular_code import send_mail
from datetime import datetime

# logging configurations 
logging.basicConfig(filename='microsoftfabric.log',
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

# merge tables to retrieve user information from the usertable 
transaction_data = transaction_table().merge(user_table(), on = 'user_id')
notification_data = user_table().merge(login_table(), on = 'user_id')

port = 587
host = 'smtp.gmail.com'
sender_email = 'abowabat@gmail.com'
sender_password = os.getenv('password')
transaction_subject = "Transaction Notification"
notification_subject = "Login Notification"

# transaction email body contents
transaction_text = """ Dear {name}
                                Guaranty Trust Bank electronic Notification Service (GeNS)
                                We wish to inform you that a {transaction_type} transaction occurred on your account.

                                Description: {transaction_type} Transaction - {date_time}
                                Amount: NGN {amount}
                                Remarks: {remark}
                                Time of Transaction: {date_time}
                                Document Number: 
                                Available Balance: NGN {balance}

                                The privacy and security of your Bank Account details is important to us. 
                                If you would prefer that we do not display your account balance in every transaction alert sent to you via email, 
                                please dial *737*51*1#.

                                Thank you for choosing Guaranty Trust Bank Limited.
                                """
transaction_html = """<html>
                        <body>
                        <p> Dear <strong>{name}</strong></p>
                                    <p> Guaranty Trust Bank electronic Notification Service (GeNS) </p>
                                    <p>We wish to inform you that a 
                                    <span style="text-transform: uppercase;">{transaction_type}</span> transaction occurred on your account.</p>
                                    <p><strong>Description:</strong> 
                                    <span style="text-transform: uppercase;">{transaction_type}</span> Transaction - {date_time}<br>
                                    <strong>Amount:</strong> NGN {amount}<br>
                                    <strong>Remarks:</strong> {remark}<br>
                                    <strong>Time of Transaction:</strong> {date_time}<br>
                                    <strong>Document Number:</strong><br>
                                    <strong>Available Balance:</strong> NGN {balance}</p>                                    
                                    <p>The privacy and security of your Bank Account details is important to us. 
                                    If you would prefer that we do not display your account balance in every transaction alert sent to you via email, 
                                    please dial *737*51*1#.</p>
                                    
                                    <p>Thank you for choosing Guaranty Trust Bank Limited.</p></body></html>"""

# notification email body contents 
notification_text = """ Dear {name},

                                    GTWORLD LOG IN CONFIRMATION

                                    Please be informed that your mobile banking profile was accessed at {date_time}
                            """
notification_html = """<html>
                    <body>
                    Dear <strong>{name}, </strong>
                                        <p><strong>GTWORLD LOG IN CONFIRMATION</strong></p>
                                        <p> Please be informed that your mobile banking profile was accessed at {date_time}. </p></body></html>"""


values = [transaction_data, notification_data, port, sender_email, sender_password, 
          host, transaction_subject, notification_subject, transaction_html, transaction_text, notification_html, notification_text]

keys = ["transaction_data", "notification_data", "port", "sender_email", "sender_password", 
          "host", "transaction_subject", "notification_subject", "transaction_html", "transaction_text", "notification_html", "notification_text"]


argument_info = dict(zip(keys, values))


