import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    auto_id = models.PositiveIntegerField(db_index=True, unique=True,null=True,blank=True)
    creator = models.ForeignKey("accounts.User", related_name="creator_%(class)s_objects", on_delete=models.CASCADE,null=True,blank=True)
    updater = models.ForeignKey("accounts.User", related_name="updator_%(class)s_objects", on_delete=models.CASCADE,null=True,blank=True)
    date_added = models.DateTimeField(db_index=True, auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True