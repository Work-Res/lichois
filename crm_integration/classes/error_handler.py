from rest_framework.response import Response
from rest_framework import status


class ErrorHandler:
    @staticmethod
    def handle_errors(errors):
        """
        Handles errors and returns an appropriate response.

        :param errors: A dictionary or list of errors.
        :return: A Response object with the errors and appropriate status code.
        """
        if errors:
            return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)
        return None

    @staticmethod
    def success(message, data=None):
        """
        Returns a success response.

        :param message: Success message.
        :param data: Additional data to include in the response.
        :return: A Response object with the success message and data.
        """
        response_data = {"message": message}
        if data:
            response_data.update(data)
        return Response(response_data, status=status.HTTP_200_OK)
