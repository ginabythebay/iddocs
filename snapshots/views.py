import os
import shutil

from distutils.dir_util import copy_tree

from django.contrib import messages
from django.conf import settings
from django.core.management import call_command
from django.shortcuts import redirect
from django.views.generic import TemplateView

from .models import Publication, Snapshot

class IndexView(TemplateView):
    template_name = 'snapshots/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        snap_query = Snapshot.objects.all()[:1]
        snap = snap_query[0] if len(snap_query) == 1 else None

        pub_query = Publication.objects.all()[:1]
        pub = pub_query[0] if len(pub_query) == 1 else None

        context.update({
            'snap': snap,
            'pub': pub,
            'messages': messages.get_messages(self.request),
        })
        return context


def create(request):
    if request.method != 'POST':
        messages.add_message(request, messages.ERROR, 'Only POST allowed.')
        return redirect('snapshots:index')

    # TODO(gina) capture output.  See
    # https://github.com/datadesk/django-bakery/issues/96
    # If no traction on the bug, some other possible solutions:
    #   * spawn a command
    #   * fork bakery
    #   * embed the relevant bits of the command into my own source
    call_command('build')
    Snapshot().save()
    messages.add_message(request, messages.INFO, 'Snapshot Created!')
    return redirect('snapshots:index')


def publish(request):
    if request.method != 'POST':
        messages.add_message(request, messages.ERROR, 'Only POST allowed.')
        return redirect('snapshots:index')

    snap_id = request.POST.get('snapshotid')
    if not snap_id:
        messages.add_message(request, messages.ERROR, 'No snapshot id found in POST.')
        return redirect('snapshots:index')

    try:
        snap = Snapshot.objects.get(pk=int(snap_id))
    except Snapshot.DoesNotExist:
        messages.add_message(request, messages.ERROR, 'Snapshot %s no longer found.  Perhaps someone created a new snapshot?' % snap_id)
        return redirect('snapshots:index')

    _clear(settings.PUBLISH_DIR)
    copy_tree(settings.BUILD_DIR, settings.PUBLISH_DIR)

    Publication.create(snap).save()
    messages.add_message(request, messages.INFO, 'Snapshot Published!')
    return redirect('snapshots:index')


def _clear(dst):
    for the_file in os.listdir(dst):
        file_path = os.path.join(folder, the_file)
        if os.path.isfile(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
