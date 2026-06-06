from django.db import models

class Attendance(models.Model):
    class Status(models.TextChoices):
        PRESENT = "PRESENT", "Present"
        ABSENT = "ABSENT", "Absent"
        LATE = "LATE", "Late"
    class DayType(models.TextChoices):
        FULL_DAY = "Full Day", "Full Day"
        THREE_QUARTER_DAY = "Three Quarter Day", "Three Quarter Day"
        HALF_DAY = "Half Day", "Half Day"
        SHORT_DAY = "Short Day", "Short Day"

    employee = models.ForeignKey(
        "employee.Employee",
        on_delete=models.CASCADE,
        related_name="attendances"
    )

    date = models.DateField()
    check_in = models.DateTimeField(
        null=True,
        blank=True
    )
    check_out = models.DateTimeField(
        null=True,
        blank=True
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.ABSENT
    )
    working_hours = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )
    day_type = models.CharField(
        max_length=20,
        choices=DayType.choices,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["employee", "date"],
                name="unique_employee_date"
            )
        ]

    def __str__(self):
        return f"{self.employee.firstname} {self.employee.lastname} - {self.date}"