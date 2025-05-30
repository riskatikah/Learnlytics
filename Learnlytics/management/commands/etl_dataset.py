#lisa
from django.core.management.base import BaseCommand
from Learnlytics.models import Student, Enrollment
import pandas as pd

class Command(BaseCommand):
    help = 'Extract data from OLTP and prepare dataset for ML training'

    def handle(self, *args, **kwargs):
        data = []
        students = Student.objects.all()

        # Loop through students and their enrollments
        for student in students:
            enrollments = Enrollment.objects.filter(stu=student)

            # For each enrollment, add a record to the data list
            for enroll in enrollments:
                label = 1 if enroll.grade >= 60 else 0  # 1 for pass, 0 for fail

                # Collect relevant data: student id, course id, grade, and whether the student passed
                data.append({
                    'stu_id': student.stu_id,
                    'course_id': enroll.course_id,
                    'grade': enroll.grade,
                    'label': label,  # This is the target variable (pass or fail)
                })

        # Save to a CSV file
        df = pd.DataFrame(data)
        df.to_csv('student_dataset.csv', index=False)
        self.stdout.write(self.style.SUCCESS(f'Dataset created with {len(data)} rows'))
