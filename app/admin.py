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
    list_display = ('otherNames', 'surname', 'programme', 'previous_programme', 'matricNumber')
    search_fields = ('otherNames', 'surname', 'matricNumber')

# Register your models here.
admin.site.register(Student)
admin.site.register(Level)
admin.site.register(College)
admin.site.register(Department)
admin.site.register(Course)
admin.site.register(Instructor)
admin.site.register(Registration)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Programme)
admin.site.register(Semester)
admin.site.register(Session)
admin.site.register(Enrollment)
admin.site.register(confirmRegister)