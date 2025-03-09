from django.utils.deprecation import MiddlewareMixin
from .utils import generate_reports

class AdminAccessMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path == '/admin/reports/report/':
            generate_reports(request.user)