from django.shortcuts import render, get_object_or_404, redirect
from itcourses_app.models import Enrollment, Student
from .forms import EnrollmentForm
from itcourses_app.management.NetworkHelper import NetworkHelper
import pandas as pd
# Create your views here.

api = NetworkHelper(base_url="http://127.0.0.1:8002/", username = "romandzo95", password = "library123")

def enrollment_list(request):
    enrollments = Enrollment.objects.all()
    return render(request, "itcourses_ui/enrollment_list.html", {"enrollments": enrollments})

def enrollment_detail(request, pk):
    enrollment = get_object_or_404(Enrollment, pk=pk)
    return render(request, "itcourses_ui/enrollment_detail.html", {"enrollment": enrollment})

def enrollment_create(request):
    if request.method == "POST":
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(enrollment_list)
    else:
        form = EnrollmentForm()
    return render(request, "itcourses_ui/enrollment_form.html", {"form": form, "mode": "create"})

def enrollment_update(request, pk):
    enrollment = get_object_or_404(Enrollment, pk=pk)
    if request.method == "POST":
        form = EnrollmentForm(request.POST, instance=enrollment)
        if form.is_valid():
            form.save()
            return redirect(enrollment_list)
    else:
        form = EnrollmentForm(instance=enrollment)
    return render(request, "itcourses_ui/enrollment_form.html", {"form": form, "mode": "update"})

def enrollment_delete(request, pk):
    enrollment = get_object_or_404(Enrollment, pk=pk)
    if request.method == "POST":
        enrollment.delete()
        return redirect(enrollment_list)
    return render(request, "itcourses_ui/enrollment_delete.html", {"enrollment": enrollment})


def external_author_list(request):
    status, data = api.get_list("authors")
    return render(request, "itcourses_ui/external_author_list.html", {"items": data})

def external_author_delete(request, pk):
    if request.method == "POST":
        api.delete_item("authors", pk)
        return redirect("external_author_list")
    
def external_book_list(request):
    status, data = api.get_list("books")
    return render(request, "itcourses_ui/external_book_list.html", {"items": data})

def external_book_delete(request, pk):
    if request.method == "POST":
        api.delete_item("books", pk)
        return redirect("external_book_list")
    
def main_view(request):
    qs = Student.objects.all().values()
    qs2 = Enrollment.objects.all().values()
    data = pd.DataFrame(qs)
    print(data)
    data2 = pd.DataFrame(qs2)
    print(data2)


    context = {
        'df': data.to_html()
    }

    return render(request, "itcourses_ui/main.html", context)