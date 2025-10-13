import os
from django.core.management.base import BaseCommand
from django.apps import apps
from django.core.files import File
from django.db.models.fields.files import FileField, ImageField


class Command(BaseCommand):
    """Migrate all local media files to Cloudinary"""

    def handle(self, *args, **kwargs):
        all_models = apps.get_models()

        for model in all_models:
            fields = [
                field for field in model._meta.get_fields()
                if isinstance(field, (FileField, ImageField))
            ]
            if not fields:
                continue

            for instance in model.objects.all():
                for field in fields:
                    file_field = getattr(instance, field.name)
                    if file_field and os.path.isfile(file_field.path):
                        with open(file_field.path, 'rb') as f:
                            file_field.save(
                                os.path.basename(file_field.path),
                                File(f),
                                save=True
                            )
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"Uploaded {field.name} for {model.__name__} (ID: {instance.pk})"
                            )
                        )
