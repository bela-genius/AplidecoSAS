from datetime import date

from django import forms

from .models import Appointment


class AppointmentForm(forms.ModelForm):
    website = forms.CharField(required=False, widget=forms.HiddenInput)  # señuelo anti-spam

    class Meta:
        model = Appointment
        fields = ["modality", "preferred_date", "preferred_slot", "full_name", "phone", "email", "message"]
        widgets = {
            "modality": forms.RadioSelect,
            "preferred_date": forms.DateInput(attrs={"type": "date"}),
            "message": forms.Textarea(attrs={"rows": 4, "placeholder": "Tipo de obra, ubicación, metros aproximados..."}),
            "full_name": forms.TextInput(attrs={"placeholder": "Tu nombre"}),
            "phone": forms.TextInput(attrs={"placeholder": "300 000 0000", "inputmode": "tel"}),
            "email": forms.EmailInput(attrs={"placeholder": "tu@correo.com (opcional)"}),
        }

    def clean_preferred_date(self):
        chosen = self.cleaned_data["preferred_date"]
        if chosen < date.today():
            raise forms.ValidationError("Elige una fecha de hoy en adelante.")
        return chosen

    def clean_website(self):
        if self.cleaned_data.get("website"):
            raise forms.ValidationError("Solicitud no válida.")
        return ""
