from django.contrib.auth.mixins import AccessMixin
from django.db import models
from django.urls import reverse_lazy


class DeletedMixin(models.Model):
    """
    Наследник будет обладать информацией об удалении
    """

    class Meta:
        abstract = True

    is_deleted = models.BooleanField(verbose_name='Удалено', default=False,
                                     db_index=True)

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        super(self.__class__, self).save(*args, **kwargs)


class StudentOrTutorRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated."""
    login_url = reverse_lazy('authapp:login')

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request, 'student') and not \
                request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class StudentRequiredMixin(AccessMixin):
    """Verify that the current user is student."""
    login_url = reverse_lazy('authapp:login_student')

    def dispatch(self, request, *args, **kwargs):
        if not request.student:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
