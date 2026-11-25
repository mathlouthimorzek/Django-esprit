from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from AccountApp.models import Doctor, Patient


class Appointment(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "En attente"
        CONFIRMED = "CONFIRMED", "Confirmé"
        CANCELLED = "CANCELLED", "Annulé"

    doctor = models.ForeignKey(
        "AccountApp.Doctor", on_delete=models.CASCADE, related_name="appointments"
    )
    patient = models.ForeignKey(
        "AccountApp.Patient", on_delete=models.CASCADE, related_name="appointments"
    )

    reason = models.TextField()
    appointment_date = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(default=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    status = models.CharField(
        max_length=9, choices=Status.choices, default=Status.PENDING
    )

    prescription = models.FileField(upload_to="prescriptions/", blank=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['doctor', 'appointment_date'],
                name='unique_doctor_appointment'
            )
        ]
        ordering = ['appointment_date']

    def clean(self):
        super().clean()
        modified_date = self._state.adding or (
            not Appointment.objects.filter(
                pk=self.pk,
                appointment_date=self.appointment_date,
            ).exists()
        )
        if self.appointment_date and modified_date and (
            self.appointment_date <= timezone.now()
        ):
            raise ValidationError(
                "Appointment date cannot be in the past."
            )