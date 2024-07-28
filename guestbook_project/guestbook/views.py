from rest_framework import generics, status
from rest_framework.response import Response
from .models import User, Entry
from .serializers import UserSerializer, EntrySerializer
from django.db.models import Count, OuterRef, Subquery
from rest_framework import viewsets
from .pagination import CustomPagination
from django.views.decorators.http import require_http_methods


class CreateEntryView(generics.CreateAPIView):
    serializer_class = EntrySerializer

    def create(self, request, *args, **kwargs):
        name = request.data.get('user')
        subject = request.data.get('subject')
        message = request.data.get('message')

        user, created = User.objects.get_or_create(name=name)
        entry = Entry.objects.create(user=user, subject=subject, message=message)

        return Response(EntrySerializer(entry).data, status=status.HTTP_201_CREATED)

class GetEntriesView(generics.ListAPIView):
    serializer_class = EntrySerializer
    pagination_class = CustomPagination

    def get_paginated_response(self, data):
        return Response({
            'count': self.queryset.count(),
            'page_size': 3,
            'total_pages': (self.queryset.count() - 1) // 3 + 1,
            'current_page_number': self.paginator.page.number,
            'links': {
                'next': self.paginator.get_next_link(),
                'previous': self.paginator.get_previous_link(),
            },
            'entries': data
        })

    def paginate_queryset(self, queryset):
        page_size = 3
        page = self.request.query_params.get('page', 1)
        return super().paginate_queryset(queryset, page_size=page_size)

class GetUsersDataView(generics.ListAPIView):
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        # Define a subquery to get the subject and message of the most recent entry
        last_entry = Entry.objects.filter(
            user=OuterRef('pk')
        ).order_by('-created_date')

        # Annotate the User queryset with the total entries, last entry subject, and message
        users_data = User.objects.annotate(
            total_entries=Count('entry'),
            last_entry_subject=Subquery(last_entry.values('subject')[:1]),
            last_entry_message=Subquery(last_entry.values('message')[:1])
        ).order_by('id').values('name', 'last_entry_subject', 'last_entry_message')

        # Format the response data
        response_data = [
            {
                'username': data['name'],
                'last_entry': f"{data['last_entry_subject']} | {data['last_entry_message']}"
            } for data in users_data
        ]

        return Response({'users': response_data})
    
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class EntryViewSet(viewsets.ModelViewSet):
    queryset = Entry.objects.all().order_by("-created_date")
    serializer_class = EntrySerializer
    pagination_class = CustomPagination