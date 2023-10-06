from django.contrib import admin
from django.urls import path
from books.views import index, schedule, book, teach_room
from users.views import login, registration, logout


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('schedule/', schedule, name='schedule'),
    path('book/', book, name='book'),
    path('teach_room/', teach_room, name='teach_room'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('registration/', registration, name='registration'),
]
