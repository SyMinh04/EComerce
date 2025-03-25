from core.logs.logging import log_info, log_error
from core.system.email.emails.account.auth import EmailRecoverPassword
from accounts.staff.repositories import StaffRepository
from accounts.user.repositories import UserRepository


class AuthEmailService:

    def send_recover_password_email(self, user_id, token, user_type):
        """
        Sen recovery password email
        @param user_id:
        @param token:
        @param user_type:
        @return:
        """

        log_info('Starting sending recovery password email to user %s with: %s' % (user_type, user_id))

        user_repo = UserRepository()

        if user_type == 'consumer':
            user_repo = UserRepository()
        elif user_type == 'staff':
            user_repo = StaffRepository()

        user = user_repo.find_by_uid(user_id)

        if not user:
            log_error('Unable to get %s with id %s' % (user_type, user_id))
        else:
            log_info('Sending recovery password email to %s id: %s) in process' % (user_type, user.email))
            email = EmailRecoverPassword(user=user, reset_password_token=token)
            email.send_email()
            log_info('Finished recovery password email to %s id: %s process' % (user_type, user.email))
