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
    path('course/delete/<str:id>', views.CourseDelete, name="course_delete"),
    path('result/filter/', views.ResultFilter, name="resultfilter"),
    path('result/view/', views.ResultView, name="resultview"),
    path('print', views.printCopy, name="print"),

    path('contact/', views.Contact, name="contact"),

    path('instructor/dashboard/', views.adminDashboard, name='instructor_dashboard'),
    path('instructor/programmes/', views.adminProgrammeManagement, name='instructor_programme_dashboard'),
    path('instructor/programmes/delete/<str:id>/', views.deleteProgramme, name='instructor_delete_programme'),
    path('instructor/programmes/upgrade/', views.UpdateProgramme, name='instructor_programme_update'),
    path('instructor/programmes/<uuid:dept>/', views.adminProgrammeDepartmentManagement, name='instructor_programme_department_dashboard'),
    path('instructor/studentlist/<uuid:dept>/<str:level>/', views.adminProgrammeDepartmentLevelManagement, name='instructor_programme_department_level_dashboard'),


    path('instructor/departments/', views.adminDepartmentManagement, name="instructorAdminDepartmentManagement"),
    path('instructor/departments/upgrade/', views.UpdateDepartment, name="instructorUpdateProgramme"),
    path('instructor/departments/delete/<str:id>/', views.deleteDepartment, name='instructordeleteDepartment'),
    path('instructor/departments/<uuid:dept>/', views.adminLevelDepartmentManagement, name='instructoradminLevelDepartmentManagement'),
    path('instructor/student/list/<uuid:dept>/<str:level>/', views.adminStudentListDepartment, name='adminStudentListDepartment'),


    path('instructor/courses/', views.CourseDept, name='instructor_course_department'),
    path('instructor/courses/<str:dept>/', views.adminCourseManagement, name='instructor_course_dashboard'),
    path('instructor/courses/<str:dept>/update/', views.updateCourse, name='instructor_course_update'),
    path('instructor/courses/delete/<str:dept>/<str:id>/', views.deleteCourse, name='instructor_delete_course'),
    path('instructor/courses/each/<str:id>/', views.eachCourse, name='instructor_each_course'),
    path('instructor/download/course-csv/', views.DownloadStudentCourse, name='instructor_course_student_download'),
    path('instructor/upload/course-csv/', views.upload_csv, name='upload_csv'),

    path('instructor/student/search/', views.registeredStudentSearchDashboard, name='instructor_student_search'),
    path('instructor/student/management/', views.registeredStudentManagementDashboard, name='instructor_student_management'),
    path('instructor/student/management/reg/delete/<str:id>/', views.deleteStudentRegisteredCourse, name='instructor_student_management_reg_delete'),
    path('instructor/student/management/reg/add/<str:matricNo>/', views.addCourseStudentRegisteredCourse, name='instructor_student_management_reg_add'),

    path('instructor/add_student/', views.manageAddStudent, name='manage_add_student'),

    path('instructor/student/reg/<str:stats>/<str:id>/', views.ApproveRejectReg, name='approve_reject_reg'),
    
    path('instructor/student/grade/', views.studentGradeUpdate, name='instructor_student_grade_update'),


    path('advisor/dashboard/', views.AdvisorDashboard, name='advisor_dashboard'),
    path('advisor/reg/', views.AdvisorReg, name='advisor_reg_matric'),
    path('advisor/students/', views.StudentList, name='advisor_student'),
    path('advisor/student/management/reg/delete/<str:id>/<str:matricNo>/', views.AdvisorDeleteStudentRegisteredCourse, name='advisor_student_management_reg_delete'),
    path('advisor/student/management/reg/add/<str:matricNo>/', views.AdvisorAddCourseStudentRegisteredCourse, name='advisor_student_management_reg_add'),
    path('advisor/student/reg/<str:stats>/<str:id>/<str:matricNo>/', views.AdvisorApproveRejectReg, name='advisor_approve_reject_reg'),

    path('success/', TemplateView.as_view(template_name='success.html'), name='success_page'),
    path('accounts/login/', views.login_view, name="login_view"),
    path('accounts/logout/', views.logout, name="logout"),
    path('accounts/changepassword/', views.changePassword, name='changepassword'),
    path('profile/', views.Profile, name='profile'),

    path('check/result/filter/', views.ParentResultFilter, name="parentresultfilter"),
    path('check/result/view/', views.ParentResultView, name="parentresultview"),



    # path('404', views.F404, name='f404')
] 


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, 
                          document_root=settings.MEDIA_ROOT)