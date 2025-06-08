from Email_notifications_variables import argument_info
from Email_notifications_modular_code import send_mail

# sends transaction email
send_mail(argument_info['port'], argument_info['host'], argument_info['sender_email'], argument_info['sender_password'], 
          argument_info['transaction_data'], argument_info['transaction_subject'], 
                          argument_info['transaction_text'], argument_info['transaction_html'])

# sends login notification email
send_mail(argument_info['port'], argument_info['host'], argument_info['sender_email'], argument_info['sender_password'], 
          argument_info['notification_data'], argument_info['notification_subject'], 
                          argument_info['notification_text'], argument_info['notification_html'])