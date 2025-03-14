from django.contrib import admin
from .models import *
from .forms import CustomUserCreationForm
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm
    
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'User role',
            {
                'fields': (
                    'user_type',
                )
            }
        )
    )
    

class StudentAdmin(admin.ModelAdmin):
    list_display = ('otherNames', 'surname', 'programme', 'matricNumber')
    search_fields = ('otherNames', 'surname', 'matricNumber', 'primaryEmail')
    list_filter = ['gender', 'entrySession', 'currentLevel', 'modeOfEntry', 'student_status', 'student_stream']


class CourseAdmin(admin.ModelAdmin):
    search_fields = ('title', 'courseCode')
    list_filter = ['unit', 'status', 'category', 'level', 'semester']

class LevelAdvisorAdmin(admin.ModelAdmin):
    search_fields = ('name')
    list_filter = ['department', 'level', 'department']

# Register your models here.
admin.site.register(Student, StudentAdmin)
admin.site.register(Level)
admin.site.register(College)
admin.site.register(Department)
admin.site.register(Course, CourseAdmin)
admin.site.register(Instructor)
admin.site.register(Registration)
admin.site.register(Result)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Programme)
admin.site.register(Semester)
admin.site.register(Session)
admin.site.register(Enrollment)
admin.site.register(confirmRegister)
admin.site.register(LevelAdvisor)