from django import forms

from .models import Expense, Category


class ExpenseSearchForm(forms.ModelForm):
    GROUPING = ('date',)
    grouping = forms.ChoiceField(
        choices=[('', '')] + list(zip(GROUPING, GROUPING))
    )
    category = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple, queryset=Category.objects.all()
    )
    #
    # sorting_by = forms.ChoiceField(
    #     choices=['date: ascending', 'date: descending', 'category: ascending', 'category: descending']
    # )

    class Meta:
        model = Expense
        fields = ('name', 'date')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = False


class CategorySearchForm(forms.Form):
    name = forms.CharField(max_length=50)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in self.fields:
            self.fields['name'].required = False
