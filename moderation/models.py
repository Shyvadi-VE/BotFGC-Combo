from django.conf import settings
from django.db import models

# ==============================================================================
# MODELOS DE MODERACIÓN (MODERATION)
# ==============================================================================


class ComboAudit(models.Model):
    """
    Registro histórico y de auditoría de los cambios de estado en los combos por parte de moderadores.

    Cardinalidades:
    - ComboAudit (N) -> (1) Combo : Muchos registros de auditoría pertenecen a un combo específico.
    - ComboAudit (N) -> (1) User  : Muchas revisiones/auditorías son realizadas por un usuario moderador.
    """
    # Cardinalidad: N:1 (Muchos registros de auditoría pertenecen a 1 combo)
    combo = models.ForeignKey(
        'combos.Combo',
        on_delete=models.CASCADE,
        related_name='audits'
    )
    # Cardinalidad: N:1 (Muchas auditorías son registradas por 1 moderador)
    moderator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    previous_status = models.CharField(max_length=20)
    new_status = models.CharField(max_length=20)
    comments = models.TextField(blank=True)
    reviewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Audit {self.id} -> Combo {self.combo_id} to {self.new_status}"
