from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls.static import static
from . import views
from django.conf import settings
from django.contrib.auth.views import LogoutView

# from .views import IndexView

urlpatterns = [
    path('', views.index, name='index'),
    # path('dashboard/', views.dashbt, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('photo-approval/', views.approval, name='approval'),
    path('profile/<str:username>', views.profile, name='profile'),
    path('photo_detail/<str:slug>', views.photo_detail, name='photo_detail'),
    path('like_post/', views.count_likes, name='like_post'),
    path('upload/', views.upload, name='upload'),
    path('video/', views.video, name='video'),
    path('my_account/', views.my_account, name='my_account'),
    path('subscription/', views.subscription, name='subscription'),
    path('image/', views.image, name='image'),
    path('about/', views.about, name='about'),
    path('music/', views.music, name='music'),
    path('login/', views.login_view, name='login'),
    path('contact/', views.contact, name='contact'),
    path('logout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    path('register/', views.register, name='register'),
    path('search/', views.SearchResultsView.as_view(), name='search'),
    path('photo-of-week/', views.pow, name='pow'),
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path("sitemap.xml", TemplateView.as_view(template_name="sitemap.xml", content_type="text/xml")),

    path('musicviews/', views.save_music_view, name='musicviews'),
    path('download/<str:type>/<slug:slug>', views.count_downloads, name='download'),
    path('imagelikes/', views.count_likes, name='imagelikes'),
    path('saveviews/', views.save_views, name='saveviews'),
    path('save_video_views/', views.save_video_views, name='save_video_views'),
    path('save_music_views/', views.save_music_view, name='save_music_views'),
    path('accounts/', include('allauth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
