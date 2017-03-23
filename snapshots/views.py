from django.contrib import messages
from django.core.management import call_command
from django.shortcuts import redirect
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'snapshots/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update({
            'messages': messages.get_messages(self.request),
        })
        return context


def create(request):
    # TODO(gina) capture output.  See
    # https://github.com/datadesk/django-bakery/issues/96
    # If no traction on the bug, some other possible solutions:
    #   * spawn a command
    #   * fork bakery
    #   * embed the relevant bits of the command into my own source
    call_command('build')
    messages.add_message(request, messages.INFO, 'Snapshot Created.')
    return redirect('snapshots:index')
