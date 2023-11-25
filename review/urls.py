
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import get_reviews, create_review, review_detail

urlpatterns = [
    path('reviews/', get_reviews, name='get_reviews'),
    path('reviews/create/', create_review, name='create_review'),
    path('reviews/<uuid:review_id>/', review_detail, name='review_detail'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)