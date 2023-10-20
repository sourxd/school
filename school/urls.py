from django.contrib import admin
from django.contrib.auth.decorators import login_required
from books.services import editor_required, teacher_required
from django.urls import path
from books.views import TeachRoomView, IndexPageView, ScheduleView, EditorView, StudentPageView, GradesView, \
    ListStudentView, AddStudentView
from users.views import login, registration, logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexPageView.as_view(), name='index'),
    path('schedule/', ScheduleView.as_view(), name='schedule'),
    path('schedule/edit/<int:class_id>/', login_required(editor_required(EditorView.as_view())), name='editor'),
    path('add_student/<int:class_id>', login_required(editor_required(AddStudentView.as_view())), name='add_student'),
    path('teach_room/', TeachRoomView.as_view(), name='teach_room'),
    path('teach_room/list_student/<int:class_id>/', ListStudentView.as_view(), name='list_student'),
    path('teach_room/list_student/<int:class_id>/<int:students_id>/<int:month_id>/', StudentPageView.as_view(),
         name='student_page'),
    path('teach_room/list_student/grades/<int:class_id>/', login_required(teacher_required(GradesView.as_view())),
         name='grades'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('registration/', registration, name='registration'),
]
