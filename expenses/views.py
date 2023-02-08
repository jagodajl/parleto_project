from django.views.generic.list import ListView

from .forms import ExpenseSearchForm
from .models import Expense, Category
from .reports import summary_per_category, summary_per_year_month


class ExpenseListView(ListView):
    model = Expense
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = object_list if object_list is not None else self.object_list

        form = ExpenseSearchForm(self.request.GET)
        if form.is_valid():
            name = form.cleaned_data.get('name', '').strip()
            if name:
                queryset = queryset.filter(name__icontains=name)

            category = form.cleaned_data.get('category')
            if category:
                queryset = queryset.filter(category__in=category)

            date = form.cleaned_data['date']
            if date:
                queryset = queryset.filter(date=date)

            grouping = form.cleaned_data['grouping']
            if grouping:
                queryset = queryset.order_by('date', '-pk')

            # sorting_by = form.cleaned_data['sorting_by']
            # if sorting_by:
            #     queryset.order_by('ascending', 'descending')


        return super().get_context_data(
            form=form,
            object_list=queryset,
            summary_per_category=summary_per_category(queryset),

            summary_per_year_month=summary_per_year_month(queryset),

            **kwargs)


class CategoryListView(ListView):
    model = Category
    paginate_by = 5
