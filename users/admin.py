from django.contrib import admin

from users.models import User, Cgroup, Subjects, Students, Ranks

admin.site.register(User)
admin.site.register(Cgroup)
admin.site.register(Subjects)
admin.site.register(Students)
admin.site.register(Ranks)