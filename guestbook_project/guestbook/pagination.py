from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):
    # Number of items per page
    page_size = 3

    def get_paginated_response(self, data):
        """
        Custom method to return paginated response with additional metadata.

        Args:
        - data (list): List of serialized data objects for the current page.

        Returns:
        - Response: Response object containing paginated data and metadata.
        """
        return Response({
            'count': self.page.paginator.count,        # Total number of items across all pages
            'page_size': self.page_size,               # Number of items per page
            'total_pages': self.page.paginator.num_pages,  # Total number of pages
            'current_page_number': self.page.number,   # Current page number
            'links': {
                'next': self.get_next_link(),          # Link to the next page
                'previous': self.get_previous_link()   # Link to the previous page
            },
            'entries': data                            # Serialized data objects for the current page
        })
