from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from Notes.views import note_list, note_detail, note_share_list, note_share_detail, register_user, CustomTokenObtainPairView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', register_user, name='register_user'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/notes/', note_list, name='note-list'),
    path('api/notes/<int:pk>/', note_detail, name='note_detail'),
    path('api/noteshares/', note_share_list, name='note_share_list'),
    path('api/noteshares/<int:pk>/', note_share_detail, name='note_share_detail'),
]
