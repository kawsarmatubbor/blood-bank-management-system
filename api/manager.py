from django.contrib.auth.models import UserManager

class CustomUserManager(UserManager):
    def create_user(self, email = None, password = None, **extra_fields):
        if not email:
            raise ValueError("User mush have an email.")
        user = self.model(email = email, **extra_fields)
        user.set_password(password)
        user.save(using = self._db)
        return user
    
    def create_superuser(self, email = None, password = None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_admin', True)
        return self.create_user(email, password)