# exceptions.py

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    # Call the default exception handler first
    response = exception_handler(exc, context)

    # If the default handler returns a response, modify it
    if response is not None:
        custom_response_data = {
            'error': True,
            'status_code': response.status_code,
            'detail': response.data  # Keep the original error detail
        }
        response.data = custom_response_data
    else:
        # If no response was generated, create a custom error response
        response = Response(
            {
                'error': True,
                'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'detail': 'An unexpected error occurred.'
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return response
