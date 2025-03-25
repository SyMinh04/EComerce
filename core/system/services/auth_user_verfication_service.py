from core.system.authentication.generators.verify_email_token_generator import AuthUserVerifyEmailTokenGenerator


class AuthUserVerificationService:
    def create_verify_email_token(self, user):
        """
        Generate reset password token
        @param user: Staff | User
        @return: string
        """
        generator = AuthUserVerifyEmailTokenGenerator()
        return generator.make_token(user)
