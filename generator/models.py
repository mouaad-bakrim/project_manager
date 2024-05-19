from django.db import models

class TypeDb(models.TextChoices):
    POSTGRES = 'postgres', 'Postgres'
    MYSQL = 'mysql', 'Mysql'

class GeneratedProject(models.Model):
    project_name = models.CharField(max_length=100)
    app = models.CharField(max_length=100, default="default_value")  # Définir une valeur par défaut ici
    application = models.TextField(default="value")
    project_path = models.CharField(max_length=255)
    type_bd = models.CharField(
        max_length=10,
        choices=TypeDb.choices,
        default=TypeDb.POSTGRES,
        db_index=True,
        verbose_name="Type de Base de Données"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.project_name
