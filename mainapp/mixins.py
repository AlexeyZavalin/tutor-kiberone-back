from django.db import models


class DeletedMixin(models.Model):
    """
    Наследник будет обладать информацией об удалении
    """

    class Meta:
        abstract = True

    is_deleted = models.BooleanField(verbose_name='Удалено', default=False, db_index=True)

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        super(self.__class__, self).save(*args, **kwargs)
