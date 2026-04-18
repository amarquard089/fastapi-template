"""Repository layer for data access logic."""

from app.infrastructure.repositories.user_repository import UserRepository, UserRepositoryDep

__all__ = ["UserRepository", "UserRepositoryDep"]
