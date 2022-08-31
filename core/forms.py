from django import forms
from .models import Exam, Question


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = [
            "name",
            "duration",
            "passing_percentage",
            "start_time",
            "end_time",
            "show_result",
        ]
        widgets = {
            "duration": forms.TimeInput(attrs={"type": "time", "step": 2}),
            "start_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = [
            "question",
            "correct_answer",
            "option_A",
            "option_B",
            "option_C",
            "option_D",
            "marks_on_correct_answer",
            "marks_on_wrong_answer",
        ]
        widgets = {"question": forms.Textarea(attrs={"rows": 5})}
