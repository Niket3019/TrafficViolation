from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("user_dashboard/", views.user_dashboard, name="user_dashboard"),
    path("pay/<int:violation_id>/", views.pay_fine, name="pay_fine"),
    path("grievance/<int:violation_id>/", views.file_grievance, name="file_grievance"),
    path("admin_dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("send_violation_email/<int:violation_id>/", views.send_violation_email, name="send_email"),
    path("update_grievance_status/", views.update_grievance_status, name="update_grievance_status"),
    path("open-gui/", views.open_gui, name="open_gui"),
    path("add-violation/", views.add_violation_view, name="add_violation"),
    path("", views.index, name=""),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)