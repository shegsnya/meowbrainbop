from django import forms
from .models import Quiz, Question, Choice
from django.forms import modelformset_factory

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['text', 'is_correct']

ChoiceFormSet = modelformset_factory(
    Choice,
    form=ChoiceForm,
    extra=4,  # lets user add 4 choices by default
    can_delete=False
)

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'time_limit_seconds']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3}),
            'time_limit_seconds': forms.NumberInput(attrs={'min': 10}),
        }
