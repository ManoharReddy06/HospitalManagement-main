from django import forms
from .models import Doctor
from hospitals.models import City, Clinic

class DoctorProfileUpdateForm(forms.ModelForm):
    city = forms.ModelChoiceField(
        queryset=City.objects.all().order_by('name'), 
        required=True, 
        empty_label="Select City",
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_city'})
    )
    clinic = forms.ModelChoiceField(
        queryset=Clinic.objects.none(), 
        required=True, 
        empty_label="Select Hospital/Clinic",
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_clinic'})
    )

    class Meta:
        model = Doctor
        fields = ['name', 'specialization', 'experience', 'consultation_fee', 'city', 'clinic', 'profile_image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'specialization': forms.TextInput(attrs={'class': 'form-control'}),
            'experience': forms.NumberInput(attrs={'class': 'form-control'}),
            'consultation_fee': forms.NumberInput(attrs={'class': 'form-control'}),
            'profile_image': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Populate clinics if city is already selected
        if 'city' in self.data:
            try:
                city_id = int(self.data.get('city'))
                self.fields['clinic'].queryset = Clinic.objects.filter(city_id=city_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.city:
            self.fields['clinic'].queryset = Clinic.objects.filter(city=self.instance.city).order_by('name')
