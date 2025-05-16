"""Second migration for bookings app."""

import django.conf
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    """Second migration class for bookings app."""

    dependencies = [
        ("bookings", "0001_initial"),
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="booking",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="bookings",
                to=django.conf.settings.AUTH_USER_MODEL,
                verbose_name="User",
            ),
        ),
    ]
