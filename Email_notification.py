import pandas as pd
from mailjet_rest import Client
import smtplib
from email.mime.text import MIMEText
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
     Retrieves the API key and secret from environment variables, 
     establishes a connection to the Mailjet API, and sends a transaction alert email.
    """
    api_key = os.getenv("api_key") 
    api_secret = os.getenv("secret_key") 

    mailjet = Client(auth=(api_key, api_secret), version='v3.1')

    transaction_details = transaction_table().merge(user_table(), on='user_id')

    if not transaction_details.empty:
        for _, row in transaction_details.iterrows():
            data = {'Messages': [{
                        "From": {"Email": "abowabat@gmail.com"},
                        "To": [{"Email": row['email'],
                                "Name": row['name']}],
                        "Subject": "Transaction Notification",
                        "TextPart": f""" Dear {row['name']}
                        Guaranty Trust Bank electronic Notification Service (GeNS)
                        We wish to inform you that a {row['transaction_type']} transaction occurred on your account.

                        Description: Electronic Money Transfer Levy - {row['date_time']}
                        Amount: NGN {row['amount']}
                        Remarks: {row['remark']}
                        Time of Transaction: {row['date_time']}
                        Document Number: 
                        Available Balance: NGN {row['balance']}

                        The privacy and security of your Bank Account details is important to us. 
                        If you would prefer that we do not display your account balance in every transaction alert sent to you via email, please dial *737*51*1#.

                        Thank you for choosing Guaranty Trust Bank Limited.
                        """,
                        "HTMLPart": f"""
                        <html>
                        <body>
                            <p>Dear {row['name']}</p>
                            <p> Guaranty Trust Bank electronic Notification Service (GeNS) </p>
                            <p>We wish to inform you that a {row['transaction_type']} transaction occurred on your account.</p>
                            <p><strong>Description:</strong> Electronic Money Transfer Levy - {row['date_time']}<br>
                            <strong>Amount:</strong> NGN {row['amount']}<br>
                            <strong>Remarks:</strong> {row['remark']}<br>
                            <strong>Time of Transaction:</strong> {row['date_time']}<br>
                            <strong>Document Number:</strong><br>
                            <strong>Available Balance:</strong> NGN {row['balance']}</p>
                            
                            <p>The privacy and security of your Bank Account details is important to us. 
                            If you would prefer that we do not display your account balance in every transaction alert sent to you via email, please dial *737*51*1#.</p>
                            
                            <p>Thank you for choosing Guaranty Trust Bank Limited.</p>
                        </body>
                        </html>
                        """}]}
        logging.info(f"sending transaction email to {row['name']}")
        result = mailjet.send.create(data=data)
        logging.info(f"email sent to {row['name']}")

    else:
        logging.info('No transactions found.')



def login_notifications():
    """
       Retrieves the API key and secret from environment variables, 
       establishes a connection to the Mailjet API, and sends a login notification email.
    """
    api_key = os.getenv("api_key") 
    api_secret = os.getenv("secret_key") 

    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    login_info = login_table().merge(user_table(), on='user_id')
    if not login_info.empty:
        for _, row in login_info.iterrows():
            data = {'Messages': [{
                        "From": {"Email": "abowabat@gmail.com"},
                        "To": [{"Email": row['email'],
                                "Name": row['name']}],
                        "Subject": "GTWorld Notification",
                        "TextPart": f""" Dear {row['name']},

                                GTWORLD LOG IN CONFIRMATION

                                Please be informed that your mobile banking profile was accessed at {row['date_time']}.""",

                        "HTMLPart": f"""
                                <html>
                                <body>
                                    <p>Dear {row['name']},</p>
                                    <p>GTWORLD LOG IN CONFIRMATION</p>
                                    <p> Please be informed that your mobile banking profile was accessed at {row['date_time']}.</p>
                                <body>
                                </html>"""}]}

        logging.info(f"sending notification email to {row['name']}")
        result = mailjet.send.create(data=data)
        logging.info(f"email sent to {row['name']}")
    else:
        logging.info('No logins found')
            

send_mail()
login_notifications()