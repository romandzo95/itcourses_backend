from django import forms
from itcourses_app.models import Student, Enrollment


class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ["enrollment_date", "student", "course"]
        widgets = {
            'enrollment_date': forms.DateInput(attrs={'type': 'date'}),
        }