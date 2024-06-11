from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        return self._create_user(username, password, **extra_fields)

    def create_agent(self, nom, prenom, email, address, username, password, **other_fields):
        other_fields.setdefault('role', 'Agent')
        other_fields.setdefault('is_superuser', False)
        other_fields.setdefault('is_staff', False)

        if other_fields.get('role') != 'Agent':
            raise ValueError('Agent must have role=Agent.')

        return self._create_user(username, password, nom=nom, prenom=prenom, email=email, address=address, **other_fields)

    def create_staffuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Staff User must have is_staff=True.')

        return self._create_user(username, password, **extra_fields)
