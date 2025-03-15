from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser
import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
import os



class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('instructor', 'Instructor'),
        ('leveladvisor', 'LevelAdvisor')
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user_type = models.CharField(max_length=15, choices=USER_TYPE_CHOICES)

   

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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
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
        return self.name + " " + str(self.id)
    
class Department(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(blank=True, null=True, max_length=500)
    college = models.ForeignKey(College, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + " " + str(self.id)


    
class Programme(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    duration = models.IntegerField(blank=True, null=True)
    degree = models.CharField(blank=True, null=True, max_length=50)

    def __str__(self):
        return self.name
    
class Level(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(blank=True, null=True, max_length=80)
    
    def __str__(self):
        return self.name


def student_passport_upload(instance, filename):
    """
    Generate a unique filename for the student's passport image.
    Format: student_<user_id>_<uuid>.<ext>
    """
    ext = filename.split('.')[-1]  # Extract file extension
    new_filename = f"student_{instance.user.id}_{uuid.uuid4().hex}.{ext}"  # Rename with user ID & UUID
    return os.path.join("images/", new_filename)


class Student(models.Model):
    STUDENTSTATUS_CHOICES = (
        ('inprogress', 'inprogress'),
        ('failed', 'failed'),
        ('graduated', 'graduated'),
    )
    STUDENTSTREAM_CJOICES = (
        ('a', 'a'),
        ('b', 'b'),
    )
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    otherNames = models.CharField(blank=True, null=True, max_length=80)
    surname = models.CharField(blank=True, null=True, max_length=80)
    currentLevel = models.ForeignKey(Level, on_delete=models.CASCADE, related_name='currentLevel',  null=True, default=1)
    matricNumber = models.CharField(blank=True, null=True, max_length=30)
    jambNumber = models.CharField(blank=True, null=True, max_length=30)
    dateOfBirth = models.DateField()
    gender = models.CharField(blank=True, null=True, max_length=15)
    studentPhoneNumber = models.CharField(blank=True, null=True, max_length=15)
    college = models.ForeignKey(College, on_delete=models.CASCADE,  null=True, default=None)
    department = models.ForeignKey(Department, on_delete=models.CASCADE,  null=True, default=None)
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE, related_name='students', blank=True, null=True)
    entrySession = models.ManyToManyField(Session, through='Enrollment', related_name='entrySession', null=True, default=None)
    currentSession = models.CharField(blank=True, null=True, max_length=20)
    primaryEmail = models.CharField(blank=True, null=True, max_length=120)
    studentEmail = models.CharField(blank=True, null=True, max_length=120)
    bloodGroup = models.CharField(blank=True, null=True, max_length=20)
    genoType = models.CharField(blank=True, null=True, max_length=20)
    modeOfEntry = models.CharField(blank=True, null=True, max_length=50)
    entryLevel =  models.ForeignKey(Level, on_delete=models.CASCADE,  null=True, default=1)
    degree = models.CharField(blank=True, null=True, max_length=50)
    nationality = models.CharField(blank=True, null=True, max_length=110)
    stateOfOrigin = models.CharField(blank=True, null=True, max_length=110)
    localGovtArea = models.CharField(blank=True, null=True, max_length=110)
    passport = models.ImageField(upload_to="images/", default='images/placeholder.png', null=True, blank=True)
    student_status =  models.CharField(blank=True, choices=STUDENTSTATUS_CHOICES, default='inprogress', null=True, max_length=100)
    student_stream = models.CharField(blank=True, choices=STUDENTSTREAM_CJOICES, default='b', null=True, max_length=100)
    
    # passport = models.ImageField(upload_to="images/")
    def __str__(self):
        return f"{self.surname} - {self.matricNumber}"

    
    def get_registered_courses(self):
        return self.registration_set.all()
    
    # def is_transitioning_to_hnd(self):
    #     # Check if the student has finished OND and is transitioning to HND
    #     return self.programme.name == 'hnd' and self.previous_programme and self.previous_programme.name == 'ond'

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    enrolled_date = models.DateField()

    def __str__(self):
        return f"{self.student} in {self.session}"
        

    
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
        ('C', 'C'),
        ('E', 'E'),
        ('R', 'R'),
    )
    CATEGORY_CHOICES = (
        ('nursing course', 'NC'),
        ('life science', 'LS'),
        ('non nursing course', 'NNC'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(blank=True, null=True, max_length=500)
    courseCode = models.CharField(blank=True, null=True, max_length=15)
    # courseDescription = models.CharField(blank=True, null=True, max_length=250)
    unit = models.IntegerField(blank=True, null=True)
    status = models.CharField(blank=True, choices=COURSE_CHOICES, default='C', null=True, max_length=40)
    category = models.CharField(blank=True, choices=CATEGORY_CHOICES, default='NNC', null=True, max_length=40)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    programme = models.ManyToManyField(Programme, related_name='courses', null=True, blank=True, default="")
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE,  null=True, default=None)

    def __str__(self):
        return f"{self.courseCode} - {self.id}"

class Instructor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(blank=True, null=True, max_length=500)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    phoneNumber = models.CharField(blank=True, null=True, max_length=15)
    departmental_email = models.CharField(blank=True, null=True, max_length=90)
    passport = models.ImageField(upload_to="images/", null=True, blank=True)

    def __str__(self):
        return self.name

class LevelAdvisor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(blank=True, null=True, max_length=500)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    passport = models.ImageField(upload_to="images/", null=True, blank=True)

    def __str__(self):
        return f'Level Advisor - {self.level.name} -{self.name}'
    


class Registration(models.Model):
    INSTRUCTOR_REMARK_CHOICES = (
        ('pending', 'pending'),
        ('approved', 'approved'),
        ('rejected', 'rejected')
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE,  null=True, default=None)
    course = models.ForeignKey(Course, on_delete=models.CASCADE,  null=True, default=None)
    session = models.ForeignKey(Session, on_delete=models.CASCADE,  null=True, default=None)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE,  null=True, default=None)
    instructor_remark = models.CharField(max_length=50, choices=INSTRUCTOR_REMARK_CHOICES, null=True, default='pending')
    registration_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} - {self.student.surname} - {self.course} ({self.session}, {self.semester})"

class Result(models.Model):
    GRADE_REMARK_CHOICES = (
        ('passed', 'passed'),
        ('failed', 'failed'),
        ('pending', 'pending'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    registration = models.ForeignKey(Registration, on_delete=models.CASCADE, related_name='results')
    attempt_number = models.PositiveIntegerField(default=1)  # Track the number of attempts (resits)
    grade = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    grade_type = models.CharField(max_length=5, null=True, blank=True)
    grade_point = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
    total_point = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
    grade_remark = models.CharField(max_length=20, choices=GRADE_REMARK_CHOICES, default='pending')
    passed = models.BooleanField(default=False)
    carried_over = models.BooleanField(default=False)
    result_date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('registration', 'attempt_number')  # Prevent duplicate attempts for the same registration

    def __str__(self):
        return f"Result for {self.registration.student.surname} - {self.registration.course} (Attempt {self.attempt_number})"

    def save(self, *args, **kwargs):
        # Automatically update grade_type based on the grade
        if self.grade is not None:
            if self.registration.course.category == 'NC' or self.registration.course.category == 'LS':
                if self.grade >= 70:
                    self.grade_type = 'A'
                elif self.grade >= 60:
                    self.grade_type = 'B'
                elif self.grade >= 50:
                    self.grade_type = 'C'
                else:
                    self.grade_type = 'F'
            else:
                if self.grade >= 70:
                    self.grade_type = 'A'
                elif self.grade >= 60:
                    self.grade_type = 'B'
                elif self.grade >= 50:
                    self.grade_type = 'C'
                elif self.grade >= 45:
                    self.grade_type = 'D'
                else:
                    self.grade_type = 'F'

            # Update grade_remark based on whether the grade is a pass or fail
            if self.registration.course.category == 'NC' or self.registration.course.category == 'LS':
                self.grade_remark = 'passed' if self.grade >= 50 else 'failed'
            else:
                self.grade_remark = 'passed' if self.grade >= 45 else 'failed'

            if self.grade_type == 'A':
                self.grade_point = 4
            elif self.grade_type == 'B':
                self.grade_point = 3
            elif self.grade_type == 'C':
                self.grade_point = 2
            elif self.grade_type == 'D':
                self.grade_point = 1
            else:
                self.grade_point = 0

        if self.grade_type is not None and self.grade_point is not None:
            self.total_point = self.grade_point * self.registration.course.unit

        super().save(*args, **kwargs)

        
class confirmRegister(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE,  null=True, default=None)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, null=True, default=None)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE,  null=True, default=None)
    registration_date = models.DateField(auto_now_add=True)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    totalUnits = models.CharField(max_length=100, blank=True, null=True)
    gpa = models.CharField(max_length=100, blank=True, null=True)

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