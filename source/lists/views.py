from django.shortcuts import redirect, render
from django.views.generic import FormView, CreateView, DetailView
from lists.models import List
from lists.forms import ExistingListItemForm, ItemForm, NewListForm
from django.contrib.auth import get_user_model
User = get_user_model()


class HomePageView(FormView):
    template_name = 'home.html'
    form_class = ItemForm


class NewListView(CreateView):
    form_class = NewListForm
    template_name = 'home.html'

    def form_valid(self, form):
        list_ = form.save(owner=self.request.user)
        return redirect(list_)


class ViewAndAddToList(DetailView, CreateView):
    model = List
    template_name = 'list.html'
    form_class = ExistingListItemForm

    def get_form(self):
        self.object = self.get_object()
        return self.form_class(for_list=self.object, data=self.request.POST)


def my_lists(request, email):
    owner = User.objects.get(email=email)
    return render(request, 'my_lists.html', {'owner': owner})
