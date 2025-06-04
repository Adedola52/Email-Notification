# Email-Notification

## CASE STUDY: Email Notification System for Transactions and logins

This project simulates a real-time email notification system used by banks and fintech platforms, built to send alerts to users immediately after a transaction or login event. It mirrors how digital banks notify users to improve transparency and prevent fraud 

## Tool Used:
- Python

## Step:
I wrote a modular Python function that sends emails to recipients using smtplib. The function accepts key parameters such as login credentials, sender credentials, email body (Plain and HTML format), and a DataFrame containing recipient details.

The function:

- Checks if the DataFrame is not empty. If it is, a log message indicates that there are no records to process
- Handles exceptions using try-except for better error tracking
- Iterates through the DataFrame to send personalized emails to each recipient
- Sends both plain text and HTML versions of the email body, allowing the recipient's email client to choose the appropriate format

The email system was used to:
- Send transaction notifications when a transaction occurs
- Send login alerts when a user logs into their account

  ![image alt](https://github.com/Adedola52/Email-Notification/blob/79006e779f6d7799302c08f955b6b58d4ab01f11/Images/Email_notification_.jpg)

