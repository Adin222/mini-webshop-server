import re


class UserUtil : 

    @staticmethod
    def check_user_email(email: str) -> bool:
        valid = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)
        return bool(valid)
    
    @staticmethod
    def check_user_password(password: str) -> bool:
        valid = re.match(r'^(?=.*[A-Z])(?=.*[^a-zA-Z0-9]).{8,}$', password)
        return bool(valid)