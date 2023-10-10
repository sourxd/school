from django.contrib import admin

from users.models import User, Cgroup, Subjects, Students

admin.site.register(User)
admin.site.register(Cgroup)
admin.site.register(Subjects)
admin.site.register(Students)