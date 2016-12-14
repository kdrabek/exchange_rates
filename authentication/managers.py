from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):

    use_in_migrations = True

    def create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError('email field is mandatory')

        user = self.model(
            email=self.normalize_email(email),
            is_admin=False,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.create_user(email, password **kwargs)
        user.is_admin = True
        user.save(using=self._db)
        return user
