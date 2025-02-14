from django.urls import path, include

urlpatterns = [
    path('v0/', include('v0.urls')),  # Route to versioned API
]
