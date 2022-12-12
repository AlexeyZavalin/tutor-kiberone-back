from mainapp.models import Student


class StudentMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if request.session.get('student'):
            try:
                request.student = Student.objects.get(
                    token=request.session.get('student')
                )
            except Student.DoesNotExist:
                pass
        else:
            request.student = None

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
