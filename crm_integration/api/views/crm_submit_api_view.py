from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from ...classes import FormSubmissionHandler, ErrorHandler


class CRMFormSubmitView(APIView):
    """
    API view to handle CRM form submissions.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handles POST requests to submit the form.

        :param request: The request object containing the form data.
        :type request: rest_framework.request.Request
        :return: Response indicating the result of the form submission.
        :rtype: rest_framework.response.Response
        """
        handler = FormSubmissionHandler(data=request.data)
        errors = handler.handle()
        error_response = ErrorHandler.handle_errors(errors)
        if error_response:
            return error_response

        return ErrorHandler.success("Form submitted successfully.")
