import os
import shutil

from distutils import dir_util

from django.contrib.auth.decorators import permission_required
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
            'snap_link': settings.BUILD_LINK,
            'pub_link': settings.PUBLISH_LINK,
            'messages': messages.get_messages(self.request),
        })
        return context

@permission_required('snapshots.can_publish')
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


@permission_required('snapshots.can_publish')
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

    _replace(settings.BUILD_DIR, settings.PUBLISH_DIR)

    Publication.create(snap).save()
    messages.add_message(request, messages.INFO, 'Snapshot Published!')
    return redirect('snapshots:index')


def _replace(src, dst):
    _clear(dst)
    # workaround for copy_tree bug.  See
    # http://stackoverflow.com/a/28055993/3075810
    #
    # TODO(gina) Move away from using dist_utils for this.
    # shutil.copytree is a candidate but it requires that the
    # destination directory not exist and I don't want to have to nuke
    # it and recreate it.  Perhaps hand-copy the top level files and
    # call shutil.copy_tree for each top level directory.  Kind of
    # like _clear, below.
    dir_util._path_created = {}
    dir_util.copy_tree(src, dst)


def _clear(dst):
    for the_file in os.listdir(dst):
        file_path = os.path.join(dst, the_file)
        if os.path.isfile(file_path):
            if the_file == ".htaccess":
                continue
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
