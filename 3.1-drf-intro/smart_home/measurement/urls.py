from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView  # Импортируем для отображения шаблона

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='home'),  # Добавляем корневой маршрут
    path('admin/', admin.site.urls)
    ]