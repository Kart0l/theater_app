"""Initial migration for shows app."""

from django.db import migrations, models


class Migration(migrations.Migration):
    """Initial migration class for shows app."""

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Show",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        auto_now_add=True,
                        db_index=True,
                        verbose_name="Created",
                    ),
                ),
                (
                    "modified",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Modified"
                    ),
                ),
                (
                    "title",
                    models.CharField(max_length=255, verbose_name="Title"),
                ),
                ("description", models.TextField(verbose_name="Description")),
                ("duration", models.DurationField(verbose_name="Duration")),
                (
                    "poster",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="shows/posters/",
                        verbose_name="Poster",
                    ),
                ),
            ],
            options={
                "verbose_name": "Show",
                "verbose_name_plural": "Shows",
                "ordering": ["-created"],
            },
        ),
    ]
