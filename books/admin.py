from django.contrib import admin

from books.models import Cgroup, Subjects, Students, Ranks

admin.site.register(Cgroup)
admin.site.register(Subjects)
admin.site.register(Students)
admin.site.register(Ranks)