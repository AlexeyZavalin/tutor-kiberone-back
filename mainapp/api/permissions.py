from rest_framework import permissions


class TutorAccessPermission(permissions.BasePermission):
    """
    permissions for tutors
    """

    def has_permission(self, request, view):
        if request.query_params.get('tutor', None):
            return bool(request.query_params.get('tutor') == request.user_id)
        else:
            return False
