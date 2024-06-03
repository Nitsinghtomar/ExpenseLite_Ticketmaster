# backend/tickets/views.py
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Ticket, Status
from .serializers import TicketSerializer, StatusSerializer, UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['post'])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.filter(username=username).first()
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        ticket = self.get_object()
        if ticket.user != request.user:
            return Response({'error': 'You can only update your own tickets.'}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        ticket = self.get_object()
        if ticket.user != request.user:
            return Response({'error': 'You can only delete your own tickets.'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = [IsAuthenticated]

@api_view(['GET'])
def report_open_vs_closed_tickets(request):
    if not request.user.is_staff:
        return Response({'error': 'Only admins can access this endpoint.'}, status=status.HTTP_403_FORBIDDEN)
    report = Ticket.objects.values('status').annotate(count=compile('status'))
    return Response(report)

@api_view(['GET'])
def report_average_resolution_time(request):
    if not request.user.is_staff:
        return Response({'error': 'Only admins can access this endpoint.'}, status=status.HTTP_403_FORBIDDEN)
    report = Status.objects.filter(status='closed').annotate(avg_resolution_time=report_average_resolution_time('changed_at'))
    return Response(report)
