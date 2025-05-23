# Email-Notification

## CASE STUDY: Email Notification System for Transactions and logins

This project simulates a real-time email notification system used by banks and fintech platforms, built to send alerts to users immediately after a transaction or login event. It mirrors how digital banks notify users to improve transparency and prevent fraud 

## Tech Stack
- Python
- Mailjet API
- dotenv for secure credentials
- Logging for error tracking

## Steps:
- Detects an events in the login and transaction tables
- It customizes the email content with relevant details like amount, time etc
- Sends email via Mailjet
- All send attempts and errors are recorded for transparency and debugging
