import logging

import traceback
from django.http import JsonResponse
from django.http import Http404
from django.utils.deprecation import MiddlewareMixin


class ApiExceptionMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        logger = logging.getLogger(__name__)

        if isinstance(exception, Http404):
            response_data = {'error': 'Resource not found'}
            return JsonResponse(response_data, status=404)
        #
        # elif isinstance(exception, PermissionDenied):
        #     response_data = {'error': 'Permission denied'}
        #     return JsonResponse(response_data, status=403)
        #
        # elif isinstance(exception, ValidationError):
        #     response_data = {'error': 'Validation error', 'details': exception.message_dict}
        #     return JsonResponse(response_data, status=400)
        #
        # elif isinstance(exception, AuthenticationFailed):
        #     response_data = {'error': 'Authentication failed', 'details': str(exception)}
        #     return JsonResponse(response_data, status=401)
        #
        else:
            # Log the exception
            logger.error(f"Exception occurred: {exception}", exc_info=True)

            # Return a JSON response with the error details
            response_data = {
                'error': 'An unexpected error occurred',
                'details': traceback.format_exc()
            }

            return JsonResponse(response_data, status=500)
