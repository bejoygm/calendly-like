from src.user.domain.models.user import User
from src.user.domain.repos.user import UserRepo


class CreateUserUsecase:
    def __init__(self, user_repo: UserRepo) -> None:
        self.repo = user_repo

    def execute(self, user: User) -> User:
        return self.repo.insert(user)
