from django.shortcuts import render
from .forms import StudentCourseForm
from Learnlytics.models import Student, Course, StudentActivityLog
import joblib
import pandas as pd

def predict_graduation(request):
    students = Student.objects.all()
    courses = Course.objects.all()

    form = StudentCourseForm(request.POST or None)
    
    prediction = None
    grade_pred = None
    confidence = None
    label = None
    pass_percentage = 0
    fail_percentage = 0

    if form.is_valid():
        stu_id = form.cleaned_data['stu_id']
        course_id = form.cleaned_data['course_id']
        
        # Get Activity Logs for the selected student
        logs = StudentActivityLog.objects.filter(stu_id=stu_id)

        total_duration = 0
        activity_count = 0

        for log in logs:
            if log.activity_end:
                duration = (log.activity_end - log.activity_start).total_seconds() / 60  # in minutes
                total_duration += duration
                activity_count += 1

        # Handle no activity case
        if activity_count == 0:
            prediction = "No activity found for this student."
        else:
            try:
                # Predict grade using grade model
                grade_model = joblib.load('grade_model.pkl')
                grade_input = pd.DataFrame([{
                    'activity_count': activity_count,
                    'total_duration': total_duration
                }])
                grade_pred = grade_model.predict(grade_input)[0]

                # Calculate pass/fail percentage based on grade prediction
                pass_percentage = 100 if grade_pred >= 60 else 0
                fail_percentage = 100 if grade_pred < 60 else 0

                # Predict graduation using course model
                course_model = joblib.load('course_model.pkl')
                course_input = pd.DataFrame([{
                    'course_id': course_id,
                    'grade': grade_pred
                }])

                label_pred = course_model.predict(course_input)[0]

                # If the model has `predict_proba`, calculate confidence
                if hasattr(course_model, "predict_proba"):
                    prob_pred = course_model.predict_proba(course_input)[0]
                    confidence = f"{max(prob_pred) * 100:.1f}%"
                else:
                    confidence = "No confidence available"

                # Set label based on prediction
                label = "PASS ✅" if label_pred == 1 else "FAIL ❌"
                prediction = f"Predicted Grade: {grade_pred:.2f}, Graduation Status: {label} (Confidence: {confidence})"
                
            except Exception as e:
                prediction = f"Error predicting graduation: {str(e)}"

    return render(request, 'Learnlytics/lisa/predict_graduations.html', {
        'form': form,
        'students': students,
        'courses': courses,
        'prediction': prediction,
        'label': label,
        'grade_pred': grade_pred,
        'confidence': confidence,
        'pass_percentage': pass_percentage,
        'fail_percentage': fail_percentage,
    })
