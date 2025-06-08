# Email-Notification

## CASE STUDY: Email Notification System for Transactions and logins

This project simulates a real-time email notification system used by banks and fintech platforms. It is designed to send alerts to users immediately after a transaction or login event, reflecting how digital banks maintain transparency and help prevent fraud.

This repository includes:

- **A modular Python script:** Defines a reusable function for sending emails using smtplib. It handles email formatting (plain and HTML), recipient iteration, and error handling
- **A configuration script:** Stores variables (e.g login credentials, sender info, email content) that are passed as arguments to the email function
- **A main driver script:** Imports both the email function and configuration, then uses them to trigger email notifications for transaction and login events

## Tool Used:
- Python

## Step:
I wrote a modular Python function that sends emails to recipients using smtplib. The function has key parameters defined such as:

- login credentials
- sender credentials
- email body (Plain and HTML format)
- DataFrame containing recipient details

The function:

- Checks if the DataFrame is not empty. If it is, a log message indicates that there are no records to process
- Handles exceptions using try-except for better error tracking
- Iterates through the DataFrame to send personalized emails to each recipient
- Sends both plain text and HTML versions of the email body, allowing the recipient's email client to choose the appropriate format

Once created, this function was called and reused in a separate Python script to send transaction and login notifications. This modular approach promotes clean code and easy reusability

The email system was used to:
- Send transaction notifications when a transaction occurs
- Send login alerts when a user logs into their account

  ![image alt](https://github.com/Adedola52/Email-Notification/blob/79006e779f6d7799302c08f955b6b58d4ab01f11/Images/Email_notification_.jpg)

  ![image alt](https://github.com/Adedola52/Email-Notification/blob/890ba0e94e0d2de86e28d835b0f774c1dd9e647f/Images/Email_notification__.jpg)

