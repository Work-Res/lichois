from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..classes import FormSubmissionHandler


class CRMFormSubmitView(APIView):
    """
    API view to handle CRM form submissions.
    """

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
        if errors:
            return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {"message": "Form submitted successfully."}, status=status.HTTP_200_OK
        )
