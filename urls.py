from django.contrib import admin
from django.urls import path
from attendance import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("kiosk/", views.kiosk, name="kiosk"),
    path("attendance/", views.attendance_page, name="attendance"),
    path("api/attendance/scan/", views.scan, name="scan"),
    path("admin/", admin.site.urls),
]
