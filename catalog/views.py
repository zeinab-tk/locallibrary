from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

import datetime

from .forms import RenewBookForm
from . import models


class Index(generic.TemplateView):

    template_name='catalog/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['num_books'] = models.Book.objects.all().count()
        context['num_instances'] = models.BookInstance.objects.all().count()
        context['num_instances_available'] = models.BookInstance.objects.filter(status__exact='a').count()
        context['num_authors'] =models.Author.objects.count()
        return context
def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("catalog:index")

class BookListView(generic.ListView):
    model=models.Book
    template_name='catalog/book_list.html'

class BookDetailView(generic.DetailView):
    model = models.Book
    template_name='catalog/book_detail.html'

class AuthorListView(generic.ListView):
    model = models.Author
    template_name = 'catalog/author_list.html'

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = models.BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return models.BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


def renew_book_librarian(request, pk):
    book_inst=get_object_or_404(models.BookInstance, pk = pk)

    if request.method == 'POST':
        form = RenewBookForm(request.POST)

        if form.is_valid():
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            return HttpResponseRedirect(reverse('catalog:my-borrowed') )

    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})

    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst':book_inst})
