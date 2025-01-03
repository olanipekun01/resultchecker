from django.urls import path, include
from . import views
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static




app_name = "resultchecker"

urlpatterns = [
    path('', views.Dashboard, name="dashboard"),
    path('courses/', views.Courses, name="course"),
    path('result/filter/', views.ResultFilter, name="resultfilter"),
    path('result/view/', views.ResultView, name="resultview"),

    path('contact/', views.Contact, name="contact"),

     path('instructor/dashboard/', views.adminDashboard, name='instructor_dashboard'),
    path('instructor/programmes/', views.adminProgrammeManagement, name='instructor_programme_dashboard'),
    path('instructor/programmes/delete/<str:id>/', views.deleteProgramme, name='instructor_delete_programme'),
    path('instructor/programmes/upgrade/', views.UpdateProgramme, name='instructor_programme_update'),


    path('instructor/courses/', views.adminCourseManagement, name='instructor_course_dashboard'),
    path('instructor/courses/update/', views.updateCourse, name='instructor_course_update'),
    path('instructor/courses/delete/<str:id>/', views.deleteCourse, name='instructor_delete_course'),
    path('instructor/courses/each/<str:id>/', views.eachCourse, name='instructor_each_course'),

    path('instructor/student/search/', views.registeredStudentSearchDashboard, name='instructor_student_search'),
    path('instructor/student/management/', views.registeredStudentManagementDashboard, name='instructor_student_management'),
    path('instructor/student/management/reg/delete/<str:id>/', views.deleteStudentRegisteredCourse, name='instructor_student_management_reg_delete'),
    path('instructor/student/management/reg/add/<str:matricNo>/', views.addCourseStudentRegisteredCourse, name='instructor_student_management_reg_add'),
    
    path('instructor/student/grade/', views.studentGradeUpdate, name='instructor_student_grade_update'),

    path('success/', TemplateView.as_view(template_name='success.html'), name='success_page'),
    path('accounts/login/', views.login_view, name="login_view"),
    path('accounts/logout/', views.logout, name="logout"),


   

    # path('404', views.F404, name='f404')
] 


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, 
                          document_root=settings.MEDIA_ROOT)