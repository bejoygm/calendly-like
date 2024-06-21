from app.user.domain.models.user import User
from app.user.domain.repos.user import UserRepo


class CreateUserUsecase:
    def __init__(self, user_repo: UserRepo):
        self.repo = user_repo

    def execute(self, user: User):
        return self.repo.insert(user)
