from django.contrib import admin
from django.urls import path
from books.views import index, schedule, book, teach_room, list_student, student_page, grades
from users.views import login, registration, logout


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('schedule/', schedule, name='schedule'),
    path('book/', book, name='book'),
    path('teach_room/', teach_room, name='teach_room'),
    path('teach_room/list_student/<int:class_id>/', list_student, name='list_student'),
    path('teach_room/list_student/<int:class_id>/<int:students_id>/<int:month_id>/', student_page, name='student_page'),
    path('teach_room/list_student/grades/<int:class_id>/', grades, name='grades'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('registration/', registration, name='registration'),
]
