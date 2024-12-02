from django.contrib.auth.base_user import BaseUserManager


class HammerSystemManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, phone, **extra_fields):
        if not phone:
            raise ValueError("Введите телефон.")
        user = self.model(phone=phone, **extra_fields)
        user.save(using=self._db)
        return user

    def create_user(self, phone, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone, **extra_fields)

    def create_superuser(self, phone, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone, **extra_fields)
