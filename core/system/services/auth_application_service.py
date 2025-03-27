from core.system.repositories import AuthApplicationRepository


class AuthApplicationService:
    repository = AuthApplicationRepository()

    def get_application(self, app_id):
        """
        Get Application by id
        """
        return self.repository.filter(client_id=app_id).first()
