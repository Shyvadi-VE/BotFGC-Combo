from django.conf import settings
from django.db import models

# ==============================================================================
# MODELOS DE COMBOS (COMBOS)
# ==============================================================================


class Combo(models.Model):
    """
    Representa un combo registrado en la plataforma.

    Cardinalidades:
    - Combo (N) -> (1) Character (point)   : Muchos combos pertenecen a un personaje principal.
    - Combo (N) -> (1) Patch               : Muchos combos pertenecen a un parche de juego específico.
    - Combo (N) -> (1) Position            : Muchos combos requieren una posición inicial específica.
    - Combo (N) -> (1) User (author)       : Muchos combos son creados por un autor/usuario.
    - Combo (N) <-> (M) Character (assists): Un combo puede usar varios personajes de asistencia y viceversa.
    - Combo (N) <-> (M) Tag                : Un combo puede tener múltiples etiquetas y una etiqueta agrupa muchos combos.
    - Combo (1) -> (N) ComboSequence       : Un combo tiene múltiples pasos ordenados de notación.
    - Combo (1) -> (N) ComboTarget         : Un combo puede tener múltiples personajes objetivos específicos.
    - Combo (1) -> (N) UserBookmark        : Un combo puede ser guardado en marcadores por múltiples usuarios.
    - Combo (1) -> (N) ComboAudit          : [App Moderation] Un combo puede tener múltiples registros de auditoría.
    """
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        APPROVED = 'APPROVED', 'Approved'
        REJECTED = 'REJECTED', 'Rejected'

    class OpponentState(models.TextChoices):
        STANDING = 'STANDING', 'Standing'
        CROUCHING = 'CROUCHING', 'Crouching'
        AIRBORNE = 'AIRBORNE', 'Airborne'
        ANY = 'ANY', 'Any'

    # Relaciones principales (Foreign Keys - Cardinalidad N:1)
    # Cardinalidad: N:1 (Muchos combos pertenecen a 1 personaje principal)
    character = models.ForeignKey(
        'catalog.Character',
        on_delete=models.CASCADE,
        related_name='point_combos'
    )
    # Cardinalidad: N:1 (Muchos combos pertenecen a 1 parche específico)
    patch = models.ForeignKey(
        'catalog.Patch',
        on_delete=models.CASCADE
    )
    # Cardinalidad: N:1 (Muchos combos requieren 1 posición en pantalla)
    position = models.ForeignKey(
        'catalog.Position',
        on_delete=models.CASCADE
    )
    # Cardinalidad: N:1 (Muchos combos son creados por 1 autor/usuario)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    # Relaciones Many-to-Many (Cardinalidad N:M)
    # Cardinalidad: N:M (Un combo puede usar 0 a N personajes de asistencia y viceversa)
    assists = models.ManyToManyField(
        'catalog.Character',
        related_name='assist_combos',
        blank=True
    )
    # Cardinalidad: N:M (Un combo puede tener múltiples tags y un tag agrupa múltiples combos)
    tags = models.ManyToManyField(
        'catalog.Tag',
        related_name='combos',
        blank=True
    )

    # Datos del combo
    raw_notation = models.TextField(blank=True)
    damage = models.IntegerField(default=0)
    opponent_state = models.CharField(
        max_length=20,
        choices=OpponentState.choices,
        default=OpponentState.ANY
    )
    resources_required = models.JSONField(default=dict, blank=True)
    is_universal_target = models.BooleanField(default=True)
    upvotes_count = models.IntegerField(default=0)
    video_url = models.URLField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Combo {self.id} - {self.character.name}"


class ComboSequence(models.Model):
    """
    Representa un paso o comando atómico dentro de la secuencia completa de un combo.

    Cardinalidades:
    - ComboSequence (N) -> (1) Combo    : Muchos pasos de secuencia pertenecen a un solo combo.
    - ComboSequence (N) -> (1) Notation : Muchos pasos de secuencia referencian una notación/comando del catálogo.
    """
    # Cardinalidad: N:1 (Muchos pasos de secuencia componen 1 combo)
    combo = models.ForeignKey(
        Combo,
        on_delete=models.CASCADE,
        related_name='sequence'
    )
    step_order = models.PositiveIntegerField()
    # Cardinalidad: N:1 (Muchos pasos de secuencia apuntan a 1 notación de movimiento)
    notation = models.ForeignKey(
        'catalog.Notation',
        on_delete=models.CASCADE
    )
    modifier = models.CharField(max_length=50, blank=True)

    class Meta:
        unique_together = ('combo', 'step_order')  # Garantiza que no se repitan pasos en el mismo combo
        ordering = ['step_order']

    def __str__(self):
        return f"Paso {self.step_order}: {self.notation.input_command} (Combo #{self.combo_id})"


class ComboTarget(models.Model):
    """
    Especifica compatibilidad con personajes particulares cuando el combo no es universal.

    Cardinalidades:
    - ComboTarget (N) -> (1) Combo     : Muchas restricciones o notas de objetivo pertenecen a un combo.
    - ComboTarget (N) -> (1) Character : Muchos objetivos específicos apuntan a un personaje del catálogo.
    """
    # Cardinalidad: N:1 (Muchas especificaciones de objetivo pertenecen a 1 combo)
    combo = models.ForeignKey(
        Combo,
        on_delete=models.CASCADE,
        related_name='specific_targets'
    )
    # Cardinalidad: N:1 (Muchas especificaciones de objetivo apuntan a 1 personaje)
    character = models.ForeignKey(
        'catalog.Character',
        on_delete=models.CASCADE
    )
    notes = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Target: {self.character.name} (Combo #{self.combo_id})"


class UserBookmark(models.Model):
    """
    Representa un combo guardado en favoritos/marcadores por un usuario.
    Funciona como tabla de unión con atributos (N:M entre User y Combo).

    Cardinalidades:
    - UserBookmark (N) -> (1) User  : Muchos marcadores pertenecen a un usuario.
    - UserBookmark (N) -> (1) Combo : Muchos marcadores referencian a un combo.
    """
    # Cardinalidad: N:1 (Muchos marcadores pertenecen a 1 usuario)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookmarks'
    )
    # Cardinalidad: N:1 (Muchos marcadores referencian a 1 combo)
    combo = models.ForeignKey(
        Combo,
        on_delete=models.CASCADE,
        related_name='bookmarked_by'
    )
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'combo')

    def __str__(self):
        return f"{self.user} -> Combo #{self.combo_id}"
