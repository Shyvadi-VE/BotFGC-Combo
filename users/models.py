from django.contrib.auth.models import AbstractUser
from django.db import models

# ==============================================================================
# MODELOS DE USUARIOS (USERS)
# ==============================================================================


class User(AbstractUser):
    """
    Representa un usuario registrado en la plataforma, extendiendo AbstractUser de Django.

    Cardinalidades:
    - User (1) -> (N) Combo         : [App Combos] Un usuario puede ser autor de múltiples combos.
    - User (1) -> (N) UserBookmark  : [App Combos] Un usuario puede guardar en marcadores múltiples combos (N:M vía UserBookmark).
    - User (1) -> (N) ComboAudit    : [App Moderation] Un usuario (moderador/admin) puede auditar múltiples combos.
    """

    # Definimos el ENUM para los roles de usuario en el sistema
    class Role(models.TextChoices):
        USER = 'USER', 'Normal User'
        MODERATOR = 'MODERATOR', 'Moderator'
        ADMIN = 'ADMIN', 'Administrator'

    # Campos heredados de AbstractUser:
    # 1. id (PK)           -> Generado automáticamente por Django
    # 2. username          -> Proporcionado por AbstractUser
    # 3. password          -> Encriptado seguro proporcionado por AbstractUser
    # 4. email             -> Proporcionado por AbstractUser
    # 5. date_joined       -> Timestamp de creación proporcionado por AbstractUser

    # Rol del usuario en la plataforma (determina permisos de moderación y administración)
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.USER
    )

    def __str__(self):
        return self.username
