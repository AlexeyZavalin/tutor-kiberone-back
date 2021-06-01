from rest_framework import permissions
from mainapp.models import Tutor


class TutorAccessPermission(permissions.BasePermission):
    """
    permissions for tutors
    """

    def has_permission(self, request, view):
        if request.query_params.get('tutor', None):
            return bool(request.user and isinstance(request.user, Tutor)
                        and request.user.pk == request.query_params.get('tutor'))
        else:
            return False
