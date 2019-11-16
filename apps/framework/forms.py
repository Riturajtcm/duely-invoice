from django import forms


class BaseModelForm(forms.ModelForm):
    required_css_class = 'req-control-label'


def get_date_field(is_required=False):
    if is_required is False:
        return forms.DateField(required=False,
                               widget=forms.TextInput(
                                   attrs={'class':
                                          'datepicker_field'}
                               ))
    else:
        return forms.DateField(required=True,
                               widget=forms.TextInput(
                                   attrs={'class': 'datepicker_field'}))


def get_default_excluded_fields():
    return ('created_on', 'deleted',
            'created_by', 'last_moddified_on',
            'last_moddified_by', 'version')
