from django.forms import ModelForm
from .models import Patient
from datetime import datetime


class PatientForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(PatientForm, self).__init__(*args, **kwargs)
        self.fields['surname'].widget.attrs = {'class': 'form-control'}
        self.fields['name'].widget.attrs = {'class': 'form-control'}
        self.fields['patronymic'].widget.attrs = {'class': 'form-control'}
        self.fields['phone'].widget.attrs = {'class': 'form-control'}
        self.fields['birth_year'].widget.attrs = {'class': 'form-control'}
        self.fields['black_list'].widget.attrs = {'class': 'form-check-input'}
        self.fields['text'].widget.attrs = {'class': 'form-control', 'rows': 5}

    class Meta:
        model = Patient
        fields = '__all__'
        localized_fields = ('birth_date',)

    def save(self, commit=True):
        instance = super(PatientForm, self).save(commit=False)
        if instance.birth_year:
            if len(instance.birth_year) == 1:
                instance.birth_year = '200' + instance.birth_year
            elif (len(instance.birth_year) == 2) and (instance.birth_year >= '0') and ('20' + instance.birth_year <= str(datetime.now().year)):
                instance.birth_year = '20' + instance.birth_year
            else:
                instance.birth_year = '19' + instance.birth_year
        if commit:
            instance.save()
        return instance
