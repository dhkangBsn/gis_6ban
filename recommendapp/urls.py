from recommendapp.views import main_html, recommend
from django.urls import path

app_name = 'recommendapp'


urlpatterns = [
    path('main_html/', main_html , name='main_html'),
    path('recommend/', recommend , name='recommend'),

]


