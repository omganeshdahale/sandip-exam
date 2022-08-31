from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MinLengthValidator, RegexValidator
from django.db import models


COLLEGE_CHOICES =(
    ("SITRC", "Sandip Institute Of Technology And Research Centre"),
    ("SIEM", "Sandip Institute Of Engineering And Management"),
    ("SU", "Sandip University"),
)

STANDARD_CHOICES = (
    ("FE", "FE"),
    ("SE", "SE"),
    ("TE", "TE"),
    ("BE", "BE"),
)

BRANCH_CHOICES = (
    ("CIVIL", "Civil Engineering"),
    ("COMP", "Computer Engineering"),
    ("EL", "Electrical Engineering"),
    ("ENTC", "Electronics and Telecommunication Engineering"),
    ("IT", "Information Technology"),
    ("ME", "Mechanical Engineering"),
    ("AI&DS", "Artificial Intelligence & Data Science"),
    ("AR", "Automation & Robotics"),
)

DIVISION_CHOICES = (
    ("A", "A"),
    ("B", "B"),
)

SEX_CHOICES = (
    ("M", "Male"),
    ("F", "Female"),
)


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_hod = models.BooleanField(default=False)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(
        max_length=10,
        validators=[
            MinLengthValidator(10),
            RegexValidator(
                regex=r'^\d*$',
                message='Only digits are allowed.'
            )
        ],
        help_text="Without dial code."
    )
    college = models.CharField(
        max_length=5,
        choices=COLLEGE_CHOICES,
        default='SITRC',
    )
    standard = models.CharField(max_length=2, choices=STANDARD_CHOICES, default="FE")
    branch = models.CharField(max_length=5, choices=BRANCH_CHOICES, default="COMP")
    division = models.CharField(max_length=1, choices=DIVISION_CHOICES, default="A")
    roll_no = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    # dob = DateField("Date of Birth")
    # sex = models.CharField(
    #     max_length=1,
    #     choices=SEX_CHOICES,
    #     default='M',
    # )
    # year_of_passing = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("college", "standard", "branch", "division", "roll_no")
        ordering = ("-created",)

    def __str__(self):
        return f"{self.standard} {self.branch} {self.division} {self.roll_no}"


class StudentRequest(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(
        max_length=10,
        validators=[
            MinLengthValidator(10),
            RegexValidator(
                regex=r'^\d*$',
                message='Only digits are allowed.'
            )
        ],
        help_text="Without dial code."
    )
    college = models.CharField(
        max_length=5,
        choices=COLLEGE_CHOICES,
        default='SITRC',
    )
    standard = models.CharField(max_length=2, choices=STANDARD_CHOICES, default="FE")
    branch = models.CharField(max_length=5, choices=BRANCH_CHOICES, default="COMP")
    division = models.CharField(max_length=1, choices=DIVISION_CHOICES, default="A")
    roll_no = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    # dob = DateField("Date of Birth")
    # sex = models.CharField(
    #     max_length=1,
    #     choices=SEX_CHOICES,
    #     default='M',
    # )
    # year_of_passing = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return f"{self.standard} {self.branch} {self.division} {self.roll_no}"


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    standard = models.CharField(max_length=2, choices=STANDARD_CHOICES, default="FE")
    branch = models.CharField(max_length=5, choices=BRANCH_CHOICES, default="COMP")
    division = models.CharField(max_length=1, choices=DIVISION_CHOICES, default="A")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("standard", "branch", "division")
        ordering = ("-created",)

    def __str__(self):
        return f"{self.standard} {self.branch} {self.division}"


class TeacherRequest(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    standard = models.CharField(max_length=2, choices=STANDARD_CHOICES, default="FE")
    branch = models.CharField(max_length=5, choices=BRANCH_CHOICES, default="COMP")
    division = models.CharField(max_length=1, choices=DIVISION_CHOICES, default="A")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return f"{self.standard} {self.branch} {self.division}"
