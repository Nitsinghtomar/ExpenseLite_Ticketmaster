# backend/backend/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from tickets.views import TicketViewSet, StatusViewSet, UserViewSet, report_open_vs_closed_tickets, report_average_resolution_time

router = DefaultRouter()
router.register(r'tickets', TicketViewSet)
router.register(r'statuses', StatusViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/reports/open-vs-closed/', report_open_vs_closed_tickets),
    path('api/reports/average-resolution-time/', report_average_resolution_time),
]
