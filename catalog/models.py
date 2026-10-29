from django.db import models

# ==============================================================================
# MODELOS DE CATÁLOGO (CATALOG)
# ==============================================================================


class Game(models.Model):
    """
    Representa un juego de peleas (FGC).

    Cardinalidades:
    - Game (1) -> (N) Patch      : Un juego tiene uno o más parches.
    - Game (1) -> (N) Character  : Un juego tiene muchos personajes.
    - Game (1) -> (N) Notation   : Un juego define muchas notaciones/movimientos.
    - Game (1) -> (N) Tag        : Un juego define múltiples etiquetas de combos.
    - Game (1) -> (N) Combo      : [App Combos] Un juego agrupa múltiples combos.
    """
    title = models.CharField(max_length=100, help_text="Ej: Guilty Gear -Strive-")
    slug = models.SlugField(unique=True, help_text="Ej: ggst")

    def __str__(self):
        return self.title


class Patch(models.Model):
    """
    Representa una versión o parche específico de un juego.

    Cardinalidades:
    - Patch (N) -> (1) Game      : Muchos parches pertenecen a un solo juego.
    - Patch (1) -> (N) Combo     : [App Combos] Un parche puede tener asociados muchos combos.
    """
    # Cardinalidad: N:1 (Muchos parches pertenecen a 1 juego)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='patches')
    version_number = models.CharField(max_length=20, help_text="Ej: 1.33")
    internal_order = models.IntegerField(help_text="Para ordenamiento matemático. Ej: 1330")
    release_date = models.DateField()
    is_current = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.game.slug} - {self.version_number}"


class Character(models.Model):
    """
    Representa un personaje jugable dentro de un juego.

    Cardinalidades:
    - Character (N) -> (1) Game      : Muchos personajes pertenecen a un solo juego.
    - Character (1) -> (N) Notation  : Un personaje puede tener múltiples notaciones específicas (0..N).
    - Character (1) -> (N) Combo     : [App Combos] Un personaje tiene asociados múltiples combos.
    """
    # Cardinalidad: N:1 (Muchos personajes pertenecen a 1 juego)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='characters')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Position(models.Model):
    """
    Representa la posición en el escenario requerida para un combo (ej: Corner, Midscreen).

    Cardinalidades:
    - Catálogo maestro independiente (reutilizable entre juegos).
    - Position (1) -> (N) Combo  : [App Combos] Una posición puede ser requerida por muchos combos.
    """
    name = models.CharField(max_length=50, help_text="Ej: Corner, Midscreen")

    def __str__(self):
        return self.name


class Notation(models.Model):
    """
    Representa un input o movimiento (normal, especial, sistema).

    Cardinalidades:
    - Notation (N) -> (1) Game        : Muchas notaciones pertenecen a un solo juego.
    - Notation (N) -> (0..1) Character: Muchas notaciones pueden pertenecer a un personaje específico,
                                         o ser universales del juego si character es null.
    - Notation (1) -> (N) ComboStep   : [App Combos] Una notación puede aparecer en múltiples pasos de combos.
    """
    # Cardinalidad: N:1 (Muchas notaciones pertenecen a 1 juego)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='notations')
    # Cardinalidad: N:1 opcional (N:0..1) - null=True permite notaciones universales como "Assist 1" o "Roman Cancel"
    character = models.ForeignKey(Character, on_delete=models.CASCADE, null=True, blank=True)
    input_command = models.CharField(max_length=50, help_text="Ej: 236P, A1")
    move_name = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=50)
    icon_url = models.URLField(blank=True)

    def __str__(self):
        return self.input_command


class Tag(models.Model):
    """
    Representa una etiqueta para clasificar combos (ej: Meter Burn, High Damage, Easy).

    Cardinalidades:
    - Tag (N) -> (1) Game        : Muchos tags pertenecen a un juego específico.
    - Tag (N) <-> (M) Combo      : [App Combos] Relación muchos a muchos; un combo tiene varios tags y viceversa.
    """
    # Cardinalidad: N:1 (Muchos tags pertenecen a 1 juego)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='tags')
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
