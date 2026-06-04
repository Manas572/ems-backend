from django.db import models

class Payslip(models.Model):
    employee = models.ForeignKey(
        "employee.Employee",
        on_delete=models.CASCADE,
        related_name="pay_slips"
    )
    month = models.PositiveSmallIntegerField()
    year = models.PositiveSmallIntegerField()
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    allowances = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["employee", "month", "year"],
                name="unique_employee_payslip"
            )
        ]

    def save(self, *args, **kwargs):
        self.net_salary = (
            self.basic_salary +
            self.allowances -
            self.deductions
        )
        super().save(*args, **kwargs)