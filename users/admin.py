from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets
    fieldsets[0][1]['fields'] += ('is_hod', 'is_teacher', 'is_student')

admin.site.register(User, UserAdmin)
admin.site.register(Student)
admin.site.register(StudentRequest)
admin.site.register(Teacher)
admin.site.register(TeacherRequest)
