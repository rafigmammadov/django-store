from django.urls import path
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.conf import settings

from users.views import login, RegisterCreateView, ProfilUpdateView, EmailVerificationView, logout

app_name = 'users'


urlpatterns = [
    path('login', login, name='login'),
    path('register', RegisterCreateView.as_view(), name='register'),
    path('profile/<int:pk>', login_required(ProfilUpdateView.as_view()), name='profile'),
    path('logout', logout, name='logout'),
    path('verify/<str:email>/<uuid:code>', EmailVerificationView.as_view(), name='email_verification')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
