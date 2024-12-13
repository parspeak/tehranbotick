from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, phone_number, first_name, last_name, password=None):
        if not phone_number:
            raise ValueError(_('Users must have an phone.'))

        if not first_name:
            raise ValueError(_('Users must have a first name.'))

        if not last_name:
            raise ValueError(_('Users must have a last name.'))

        user = self.model(
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, first_name, last_name, password=None):
        user = self.create_user(
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user
