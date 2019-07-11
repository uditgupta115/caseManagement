from django.forms import ModelForm

from casemanagement.casesystem.models import Case


class CaseForm(ModelForm):
    class Meta:
        model = Case
        fields = '__all__'
