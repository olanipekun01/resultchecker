from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser
import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now



class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('instructor', 'Instructor'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # date_joined = models.DateTimeField(auto_now_add=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

    # groups = models.ManyToManyField(
    #     'auth.Group',
    #     related_name='customuser_set',  # Custom related name to avoid conflict
    #     blank=True
    # )
    # user_permissions = models.ManyToManyField(
    #     'auth.Permission',
    #     related_name='customuser_permissions_set',  # Custom related name to avoid conflict
    #     blank=True
    # )

    def __str__(self):
        return self.username
        
    def set_password(self, raw_password):
        """Hash and set the password."""
        self.password = make_password(raw_password)
        self.save()
        
    def check_password(self, raw_password):
        """Check the password against the stored hashed password."""
        return check_password(raw_password, self.password)

class Session(models.Model):
    year = models.CharField(max_length=9)  # e.g., '2023/2024'
    is_current = models.BooleanField(default=False)  # Marks current active session

    def save(self, *args, **kwargs):
        if self.is_current:
            # Uncheck `is_current` for all other Semester objects
            Session.objects.filter(is_current=True).exclude(id=self.id).update(is_current=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.year
    
    

class College(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(blank=True, null=True, max_length=500)

    def __str__(self):
        return self.name
    
class Department(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(blank=True, null=True, max_length=500)
    college = models.ForeignKey(College, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

# class Programme(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     name = models.CharField(blank=True, null=True, max_length=500)
#     department = models.ForeignKey(Department, on_delete=models.CASCADE)
#     duration = models.IntegerField(blank=True, null=True)
#     degree = models.CharField(blank=True, null=True, max_length=50)

#     def __str__(self):
#         return self.name
    
class Programme(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    PROGRAMME_CHOICES = (
        ('ond', 'OND Nursing'),
        ('hnd', 'HND Nursing'),
    )
    name = models.CharField(max_length=20, choices=PROGRAMME_CHOICES, unique=True, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    duration = models.IntegerField(blank=True, null=True)
    degree = models.CharField(blank=True, null=True, max_length=50)

    def __str__(self):
        return self.get_name_display()


class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    otherNames = models.CharField(blank=True, null=True, max_length=80)
    surname = models.CharField(blank=True, null=True, max_length=80)
    currentLevel = models.CharField(blank=True, null=True, max_length=80)
    matricNumber = models.CharField(blank=True, null=True, max_length=30)
    jambNumber = models.CharField(blank=True, null=True, max_length=30)
    dateOfBirth = models.DateField()
    gender = models.CharField(blank=True, null=True, max_length=15)
    studentPhoneNumber = models.CharField(blank=True, null=True, max_length=15)
    college = models.ForeignKey(College, on_delete=models.CASCADE,  null=True, default=None)
    department = models.ForeignKey(Department, on_delete=models.CASCADE,  null=True, default=None)
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE, related_name='students', blank=True, null=True)
    previous_programme = models.ForeignKey(Programme, on_delete=models.SET_NULL, null=True, blank=True, related_name='students_with_previous_programme')
    entrySession = models.ManyToManyField(Session, through='Enrollment', related_name='entrySession', null=True, default=None)
    currentSession = models.CharField(blank=True, null=True, max_length=20)
    primaryEmail = models.CharField(blank=True, null=True, max_length=120)
    studentEmail = models.CharField(blank=True, null=True, max_length=120)
    bloodGroup = models.CharField(blank=True, null=True, max_length=20)
    genoType = models.CharField(blank=True, null=True, max_length=20)
    modeOfEntry = models.CharField(blank=True, null=True, max_length=50)
    entryLevel = models.CharField(blank=True, null=True, max_length=50)
    degree = models.CharField(blank=True, null=True, max_length=50)
    # bloodgroup, genotype, jambreg,email, 
    # maritalStatus = models.CharField(blank=True, null=True, max_length=30)
    nationality = models.CharField(blank=True, null=True, max_length=110)
    stateOfOrigin = models.CharField(blank=True, null=True, max_length=110)
    localGovtArea = models.CharField(blank=True, null=True, max_length=110)
    passport = models.ImageField(upload_to="images/", null=True, blank=True)

    
    # passport = models.ImageField(upload_to="images/")
    def __str__(self):
        return f"{self.surname} - {self.matricNumber}"

    
    def get_registered_courses(self):
        return self.registration_set.all()
    
    def is_transitioning_to_hnd(self):
        # Check if the student has finished OND and is transitioning to HND
        return self.programme.name == 'hnd' and self.previous_programme and self.previous_programme.name == 'ond'

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    enrolled_date = models.DateField()

    def __str__(self):
        return f"{self.student} in {self.session}"
        
class Level(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(blank=True, null=True, max_length=80)
    
    def __str__(self):
        return self.name
    
class Semester(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(blank=True, null=True, max_length=80)
    is_current = models.BooleanField(default=False) 
    
    def save(self, *args, **kwargs):
        if self.is_current:
            # Uncheck `is_current` for all other Semester objects
            Semester.objects.filter(is_current=True).exclude(id=self.id).update(is_current=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    


class Course(models.Model):
    COURSE_CHOICES = (
        ('compulsory', 'C'),
        ('elective', 'E'),
        ('recommendation', 'R'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(blank=True, null=True, max_length=500)
    courseCode = models.CharField(blank=True, null=True, max_length=15)
    # courseDescription = models.CharField(blank=True, null=True, max_length=250)
    unit = models.IntegerField(blank=True, null=True)
    status = models.CharField(blank=True, choices=COURSE_CHOICES, default='C', null=True, max_length=40)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE, related_name='courses', null=True, blank=True, default="")
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE,  null=True, default=None)

    def __str__(self):
        return f"{self.courseCode} - {self.title}"

class Instructor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(blank=True, null=True, max_length=500)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    phoneNumber = models.CharField(blank=True, null=True, max_length=15)
    departmental_email = models.CharField(blank=True, null=True, max_length=90)
    passport = models.ImageField(upload_to="images/", null=True, blank=True)

    def __str__(self):
        return self.name

class Registration(models.Model):
    GRADE_REMARK_CHOICES = (
        ('passed', 'passed'),
        ('failed', 'failed'),
        ('pending', 'pending'),
    )

    INSTRUCTOR_REMARK_CHOICES = (
        ('pending', 'pending'),
        ('approved', 'approved'),
        ('rejected', 'rejected')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, default=None)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, default=None)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, null=True, default=None)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, null=True, default=None)
    registration_date = models.DateField(auto_now_add=True)
    passed = models.BooleanField(default=False)
    carried_over = models.BooleanField(default=False)
    grade = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)
    grade_type = models.CharField(max_length=5, null=True, default='...')
    grade_remark = models.CharField(max_length=20, choices=GRADE_REMARK_CHOICES, null=True, default='pending')
    instructor_remark = models.CharField(max_length=20, choices=INSTRUCTOR_REMARK_CHOICES, null=True, default='pending')

    def __str__(self):
        return f"{self.student.surname} - {self.registration_date}"

    def save(self, *args, **kwargs):
        # Automatically update grade_type based on the grade
        if int(self.grade) is not None:
            if int(self.grade) >= 70:
                self.grade_type = 'A'
            elif int(self.grade) >= 60:
                self.grade_type = 'B'
            elif int(self.grade) >= 50:
                self.grade_type = 'C'
            elif int(self.grade) >= 45:
                self.grade_type = 'D'
            elif int(self.grade) >= 40:
                self.grade_type = 'E'
            else:
                self.grade_type = 'F'

            # Update grade_remark based on whether the grade is a pass or fail
            if int(self.grade) >= 40:  # Assuming 40 is the passing grade
                self.grade_remark = 'passed'
            elif int(self.grade) <= 0:
                self.grade_remark = 'pending'
            else:
                self.grade_remark = 'failed'
        
        # Call the original save method
        super().save(*args, **kwargs)

        
class confirmRegister(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE,  null=True, default=None)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, null=True, default=None)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE,  null=True, default=None)
    registration_date = models.DateField(auto_now_add=True)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    totalUnits = models.CharField(max_length=100, blank=True, null=True)

@receiver(post_save, sender=Student)
def create_enrollment_for_student(sender, instance, created, **kwargs):
    if created:  # Check if it's a new Student instance
        try:
            # Get the current session
            current_session = Session.objects.get(is_current=True)

            # Create an Enrollment entry for the student
            Enrollment.objects.create(
                student=instance,
                session=current_session,
                enrolled_date=now()
            )
        except Session.DoesNotExist:
            # Handle case where no current session exists
            print("No current session found for enrollment.")