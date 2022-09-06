import io
import xlwt
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import FileResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from core.decorators import *
from core.models import Exam, Session
from users.models import Student, StudentRequest

User = get_user_model()


@login_required
@is_verified_teacher
def students_list(request):
    teacher = request.user.teacher
    search = request.GET.get("search", None)
    students = User.objects.filter(
        student__college=teacher.college,
        student__branch=teacher.branch,
    )
    if search:
        students = students.filter(Q(username__icontains=search) | Q(email__icontains=search))

    paginator = Paginator(students, 15)
    page = request.GET.get("page")
    try:
        students = paginator.page(page)
    except PageNotAnInteger:
        students = paginator.page(1)
    except EmptyPage:
        students = paginator.page(paginator.num_pages)

    return render(request, "teachers/students_list.html", {"students": students})


@require_POST
@login_required
@is_verified_teacher
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    teacher = request.user.teacher
    if (
        student.college != teacher.college
        or student.branch != teacher.branch
    ):
        raise PermissionDenied()

    student.delete()
    messages.success(request, "Profile deleted successfully")

    return redirect("teachers:students_list")


@login_required
@is_verified_teacher
def students_request_list(request):
    teacher = request.user.teacher
    search = request.GET.get("search", None)
    students = User.objects.filter(
        studentrequest__college=teacher.college,
        studentrequest__branch=teacher.branch,
    )
    if search:
        students = students.filter(Q(username__icontains=search) | Q(email__icontains=search))

    paginator = Paginator(students, 15)
    page = request.GET.get("page")
    try:
        students = paginator.page(page)
    except PageNotAnInteger:
        students = paginator.page(1)
    except EmptyPage:
        students = paginator.page(paginator.num_pages)

    return render(
        request, "teachers/students_request_list.html", {"students": students}
    )


@require_POST
@login_required
@is_verified_teacher
def student_request_accept(request, pk):
    studentrequest = get_object_or_404(StudentRequest, pk=pk)
    teacher = request.user.teacher
    if (
        studentrequest.college != teacher.college
        or studentrequest.branch != teacher.branch
    ):
        raise PermissionDenied()

    if Student.objects.exclude(user=None).filter(prn=studentrequest.prn).exists():
        messages.error(
            request,
            f"Profile with PRN {studentrequest.prn} already exists, please delete it first",
        )
    else:
        Student.objects.create(
            user=studentrequest.user,
            full_name=studentrequest.full_name,
            email=studentrequest.email,
            phone=studentrequest.phone,
            college=studentrequest.college,
            standard=studentrequest.standard,
            branch=studentrequest.branch,
            prn=studentrequest.prn,
        )
        studentrequest.delete()
        messages.success(request, "Profile request accepted")

    return redirect("teachers:students_request_list")


@login_required
@is_verified_teacher
def result_list(request, exam_pk):
    exam = get_object_or_404(Exam, pk=exam_pk)
    if exam.user != request.user:
        raise PermissionDenied()
    sessions = exam.session_set.filter(completed=True)
    active_sessions = exam.session_set.filter(completed=False).count()

    paginator = Paginator(sessions, 15)
    page = request.GET.get("page")
    try:
        sessions = paginator.page(page)
    except PageNotAnInteger:
        sessions = paginator.page(1)
    except EmptyPage:
        sessions = paginator.page(paginator.num_pages)

    context = {
        "exam": exam,
        "sessions": sessions,
        "active_sessions": active_sessions,
    }
    return render(request, "teachers/result_list.html", context)


@login_required
@is_verified_teacher
def result_list_export_excel(request, exam_pk):
    exam = get_object_or_404(Exam, pk=exam_pk)
    if exam.user != request.user:
        raise PermissionDenied()
    sessions = exam.session_set.filter(completed=True).select_related("student", "exam")

    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet("Results")
    worksheet.write(0, 0, "PRN")
    worksheet.write(0, 1, "STUDENT NAME")
    worksheet.write(0, 2, "COLLEGE")
    worksheet.write(0, 3, "STANDARD")
    worksheet.write(0, 4, "BRANCH")
    worksheet.write(0, 5, "ATTEMPTED QUESTIONS")
    worksheet.write(0, 6, "TOTAL QUESTIONS")
    worksheet.write(0, 7, "MARKS OBTAIN")
    worksheet.write(0, 8, "MAX MARKS")
    worksheet.write(0, 9, "PASSING PERCENTAGE")
    worksheet.write(0, 10, "PASSING STATUS")
    worksheet.write(0, 11, "SUBMITTED ON")

    for row, session in enumerate(sessions, start=1):
        worksheet.write(row, 0, session.student.prn)
        worksheet.write(row, 1, session.student.full_name)
        worksheet.write(row, 2, session.student.get_college_display())
        worksheet.write(row, 3, session.student.get_standard_display())
        worksheet.write(row, 4, session.student.get_branch_display())
        worksheet.write(row, 5, session.get_num_attempted_que())
        worksheet.write(row, 6, session.get_num_total_que())
        worksheet.write(row, 7, session.get_marks())
        worksheet.write(row, 8, session.get_max_marks())
        worksheet.write(row, 9, session.exam.passing_percentage)
        passing_status = session.get_passing_status()
        passing_status = "PASS" if passing_status else "FAIL"
        worksheet.write(row, 10, passing_status)
        worksheet.write(row, 11, session.submitted.strftime("%m/%d/%Y"))

    buffer = io.BytesIO()
    workbook.save(buffer)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename="report.xlsx")


@login_required
@is_verified_teacher
def result_detail(request, pk):
    session = get_object_or_404(Session, pk=pk, completed=True)
    if session.exam.user != request.user:
        raise PermissionDenied()

    search = request.GET.get("search", None)
    if search:
        answers = session.answer_set.filter(
            question__question__icontains=search
        ).order_by("question__created")
    else:
        answers = session.answer_set.all().order_by("question__created")

    paginator = Paginator(answers, 15)
    page = request.GET.get("page")
    try:
        answers = paginator.page(page)
    except PageNotAnInteger:
        answers = paginator.page(1)
    except EmptyPage:
        answers = paginator.page(paginator.num_pages)

    context = {"session": session, "answers": answers}
    return render(request, "teachers/result_detail.html", context)
