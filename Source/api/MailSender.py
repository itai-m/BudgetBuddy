from google.appengine.api import mail


class MailSender:
    __Budget_Buddy_Signature = "\nBudgetBuddy. Copyright 2015"
    __Budget_Buddy_Formal_Address = "BudgetBuddy <budgetbuddy00@gmail.com>"

    def __init__(self):
        pass

    @staticmethod
    def send_invite_friend(from_user_name, to_address):
        body = """
        Hello,
        The user {0} has invited you to join BudgetBuddy!
        to join please register through the following form:
        http://budgetbuddy001.appspot.com/Registration
        """.format(from_user_name)
        MailSender.__send_email(from_user_name + " <" + to_address + ">", "A friend as invite you", body)

    @staticmethod
    def send_password_recovery_token(to_user_name, to_address, to_token):
        body = """
        Hello,
        Please go to http://budgetbuddy001.appspot.com/PasswordRecovery/{0}
        You will get your new password within a minute after click the link
        """.format(to_token)
        MailSender.__send_email(to_user_name + " <" + to_address + ">", "Password Recovery", body)

    @staticmethod
    def send_new_password(to_user_name, to_address, to_pass):
        body = """
        Hello,
        Your new password has been set to {0}
        You can login through our login page in http://budgetbuddy001.appspot.com/Login
        with your username and new password
        """.format(to_pass)
        MailSender.__send_email(to_user_name + " <" + to_address + ">", "Password Recovery", body)

    @staticmethod
    def check_if_email_valid(email_address):
        return mail.is_email_valid(email_address)

    @staticmethod
    def __send_email(to_email, subject, body):
        mail.send_mail(sender=MailSender.__Budget_Buddy_Formal_Address,
                       to=to_email,
                       subject=subject,
                       body=body + MailSender.__Budget_Buddy_Signature
                       )
