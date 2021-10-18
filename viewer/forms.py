import re
from datetime import date

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, HTML
from django.core.exceptions import ValidationError
from django.forms import (DateField, ModelForm)

from viewer.models import Movie

def capitalized_validator(value):
    if value[0].islower():
        raise ValidationError('Value must be capitalized!')


class PastMonthField(DateField):

    def validate(self, value):
        super().validate(value)
        if value >= date.today():
            raise ValidationError('Only past dates allowed here')

    def clean(self, value):
        result = super().clean(value)
        return date(year=result.year, month=result.month, day=1)

class MovieForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'title',
            HTML('<strong>miedzy tytulem a reszta</strong>'),
            Row(Column('genre'), Column('rating'), Column('released')),
            'description', 'poster',
            Submit('submit', 'Submit'),
        )

    class Meta:
        model = Movie
        fields = '__all__'




    def clean_description(self):
        # Force each sentence of the description to be capitalized.
        initial = self.cleaned_data['description']
        sentences = re.sub(r'\s*\.\s*', '.', initial).split('.')
        return '. '.join(sentence.capitalize() for sentence in sentences)


    def clean(self):
        result = super().clean()
        if result['genre'].name == 'Comedy' and result['rating'] > 5:
            self.add_error('genre', 'Wrong Genre')
            self.add_error('rating', '')
            raise ValidationError(
                "Comedies aren't so good to be rated over 5."
            )
        return result
