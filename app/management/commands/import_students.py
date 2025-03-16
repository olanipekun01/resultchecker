import csv
import os
import uuid
from datetime import datetime
from django.core.management.base import BaseCommand
from django.core.files import File
from app.models import CustomUser, Student, Level, College, Department, Programme, Session, Enrollment

class Command(BaseCommand):
    help = 'Import students from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']
        
        if not os.path.exists(csv_file_path):
            self.stdout.write(self.style.ERROR(f"File {csv_file_path} does not exist"))
            return

        try:
            with open(csv_file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                required_columns = {
                    'surname', 'otherNames', 'matricNumber', 
                    'dateOfBirth', 'gender', 'currentLevel', 'department', 
                    'programme', 'currentSession'
                }
                if not all(col in reader.fieldnames for col in required_columns):
                    missing = required_columns - set(reader.fieldnames)
                    self.stdout.write(self.style.ERROR(f"Missing required columns: {missing}"))
                    return

                success_count = 0
                error_count = 0

                for row in reader:
                    try:
                        # Create CustomUser first
                        user = CustomUser(
                            id=uuid.uuid4(),
                            username=row['primaryEmail'],
                            user_type='student'
                        )
                        # Set a default password (e.g., matric number)
                        user.set_password(row['matricNumber'])
                        user.save()

                        # Get related objects
                        current_level = Level.objects.get(name=row['currentLevel'])  # or name=
                        department = Department.objects.get(name=row['department'])  # or name=
                        programme = Programme.objects.get(name=row['programme'])  # or name=

                        # Parse date of birth (assuming format: YYYY-MM-DD)
                        dob = datetime.strptime(row['dateOfBirth'], '%Y-%m-%d').date()

                        # Create Student
                        student = Student(
                            user=user,
                            surname=row['surname'],
                            otherNames=row['otherNames'],
                            currentLevel=current_level,
                            matricNumber=row['matricNumber'],
                            jambNumber=row.get('jambNumber', None),
                            dateOfBirth=dob,
                            gender=row['gender'],
                            studentPhoneNumber=row.get('studentPhoneNumber', None),
                            department=department,
                            programme=programme,
                            currentSession=row['currentSession'],
                            primaryEmail=row.get('primaryEmail', None),
                            studentEmail=row.get('studentEmail', None),
                            bloodGroup=row.get('bloodGroup', None),
                            genoType=row.get('genoType', None),
                            modeOfEntry=row.get('modeOfEntry', None),
                            entryLevel=Level.objects.get(name=row.get('entryLevel', row['currentLevel'])),
                            degree=row.get('degree', None),
                            nationality=row.get('nationality', None),
                            stateOfOrigin=row.get('stateOfOrigin', None),
                            localGovtArea=row.get('localGovtArea', None),
                            student_status=row.get('student_status', 'inprogress'),
                            student_stream=row.get('student_stream', 'b')
                        )

                        # Handle college if provided
                        if 'college' in row and row['college']:
                            student.college = College.objects.get(name=row['college of nursing akure'])

                       

                        student.save()

                        # Handle entrySession if provided (comma-separated session IDs)
                        if 'entrySession' in row and row['entrySession']:
                            sessions = row['entrySession'].split(',')
                            for session_id in sessions:
                                try:
                                    session = Session.objects.get(year=session_id.strip())
                                    Enrollment.objects.create(
                                        student=student,
                                        session=session
                                    )
                                except Session.DoesNotExist:
                                    self.stdout.write(self.style.WARNING(
                                        f"Session {session_id} not found for {student.matricNumber}"
                                    ))

                        success_count += 1
                        self.stdout.write(self.style.SUCCESS(
                            f"Successfully imported student: {student.matricNumber}"
                        ))

                    except Exception as e:
                        self.stdout.write(self.style.ERROR(
                            f"Error importing student {row.get('matricNumber', 'unknown')}: {str(e)}"
                        ))
                        error_count += 1

                self.stdout.write(self.style.SUCCESS(
                    f"Import completed: {success_count} students imported, {error_count} errors"
                ))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error reading CSV file: {str(e)}"))
