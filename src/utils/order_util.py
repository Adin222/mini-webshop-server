import re
import smtplib
from ..schemas.order_schemas import OrderCreation
from settings import APP_PASSWORD
from email.message import EmailMessage

class OrderUtil:
    @staticmethod
    def valid_order_data(order_data) -> bool:
        if not order_data.name or order_data.name.strip() == "":
            return False

        if not order_data.last_name or order_data.last_name.strip() == "":
            return False

        if not order_data.phone or order_data.phone.strip() == "":
            return False
        
        return True
    
    @staticmethod
    def is_valid_phone(phone: str) -> bool:
        return bool(re.fullmatch(r'[+\-\d\s]{6,20}', phone))
    
    
    @staticmethod
    def send_dummy_email(to_email: str, buyer_data: OrderCreation):
        sender = "adincustovic121@gmail.com"
        password = APP_PASSWORD

        msg = EmailMessage()
        msg['Subject'] = "New order has arrived"
        msg['From'] = sender
        msg['To'] = to_email

        msg.set_content(f"""\
Dear Sir/Madam,

A new order has been received with the following customer details:

Name and lastname: {buyer_data.name} {buyer_data.last_name}
Phone: {buyer_data.phone}
Address: {buyer_data.address}
Email: {buyer_data.email if buyer_data.email else 'Buyer did not specify'}

Please proceed with the next steps.

Best regards,
Your order system
""")

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender, password)
            server.send_message(msg)

