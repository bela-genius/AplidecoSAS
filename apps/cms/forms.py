from datetime import date

from django import forms

from .models import Appointment

SERVICES = [
    "Pintura de fachada",
    "Impermeabilización",
    "Estuco y acabados",
    "Sellado de filtraciones",
    "Otro / aún no lo sé",
]


class AppointmentForm(forms.ModelForm):
    website = forms.CharField(required=False)  # señuelo anti-spam: debe quedar vacío
    service = forms.ChoiceField(choices=[(s, s) for s in SERVICES], initial=SERVICES[0])

    class Meta:
        model = Appointment
        fields = ["modality", "service", "preferred_date", "preferred_slot", "full_name", "phone"]

    def clean_preferred_date(self):
        chosen = self.cleaned_data.get("preferred_date")
        if chosen and chosen < date.today():
            raise forms.ValidationError("Elige una fecha de hoy en adelante.")
        return chosen

    def clean_website(self):
        if self.cleaned_data.get("website"):
            raise forms.ValidationError("Solicitud no válida.")
        return ""
