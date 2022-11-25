from django.contrib.contenttypes.models import ContentType
from django.db import models


class BaseModel(models.Model):
    """Base class for (almost) all models

    NOTE: Should always be the last (right-most) element in the inheritance chain.
    """
    class Meta:
        abstract = True

    def clean_save(self, *args, **kwargs):
        """
        Call the super.save() method of the object instead of the normal save.
        This can be useful if you only want to save fields without any side effects.
        """
        super().save(*args, **kwargs)

    @property
    def contenttype(self) -> ContentType:
        return self.get_contenttype()

    @classmethod
    def get_contenttype(cls) -> ContentType:
        return ContentType.objects.get_for_model(cls)
