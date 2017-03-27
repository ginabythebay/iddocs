import os
import shutil

import errno

from django.contrib.admin.models import LogEntry, ADDITION
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.management import call_command
from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.utils.encoding import force_unicode
from django.views.generic import TemplateView

from .models import Publication, Snapshot


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'snapshots/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        snap_query = Snapshot.objects.all()[:1]
        snap = snap_query[0] if len(snap_query) == 1 else None

        snap_log = _read_log() if snap else None

        pub_query = Publication.objects.all()[:1]
        pub = pub_query[0] if len(pub_query) == 1 else None

        context.update({
            'has_permission': True,
            'snap': snap,
            'snap_log': snap_log,
            'pub': pub,
            'snap_link': settings.BUILD_LINK,
            'pub_link': settings.PUBLISH_LINK,
            'messages': messages.get_messages(self.request),
        })
        return context


def test_auth(request):
    return HttpResponse('Hello test_auth world. HTTP_AUTH=[%s]' %
                        request.META.get('HTTP_AUTHORIZATION', ''))


@permission_required('snapshots.can_publish')
def create(request):
    if request.method != 'POST':
        messages.add_message(request, messages.ERROR, 'Only POST allowed.')
        return redirect('snapshots:index')

    _build()
    snap = Snapshot()
    snap.save()

    LogEntry.objects.log_action(
        user_id=request.user.pk,
        content_type_id=ContentType.objects.get_for_model(snap).pk,
        object_id=snap.pk,
        object_repr=force_unicode('snapshot %s ' % snap.pk),
        action_flag=ADDITION
    )
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

    pub = Publication.create(snap)
    pub.save()

    LogEntry.objects.log_action(
        user_id=request.user.pk,
        content_type_id=ContentType.objects.get_for_model(pub).pk,
        object_id=pub.pk,
        object_repr=force_unicode('publication %s' % snap.pk),
        action_flag=ADDITION
    )
    messages.add_message(request, messages.INFO, 'Snapshot Published!')
    return redirect('snapshots:index')


def _read_log():
    try:
        with open(os.path.join(settings.BUILD_TMP_DIR, 'staging.out'),
                  'r') as f:
            return f.read()
    except IOError as exc:
        if exc.errno == errno.ENOENT:
            return '[no log file found]'
        else:
            raise


def _build():
    try:
        os.makedirs(settings.BUILD_TMP_DIR)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(settings.BUILD_TMP_DIR):
            pass
        else:
            raise
    with open(os.path.join(settings.BUILD_TMP_DIR, 'staging.out'), 'w') as out:
        call_command('build', '--verbosity', 2, stdout = out, stderr = out)


def _replace(src, dst):
    _clear(dst)
    _copy_tree(src, dst)


def _copy_tree(src, dst):
    """Like shutil.copytree, but expects that dst exists."""
    for the_file in os.listdir(src):
        src_file = os.path.join(src, the_file)
        dst_file = os.path.join(dst, the_file)
        if os.path.isfile(src_file):
            shutil.copyfile(src_file, dst_file)
        elif os.path.isdir(src_file):
            shutil.copytree(src_file, dst_file)


def _clear(dst):
    for the_file in os.listdir(dst):
        file_path = os.path.join(dst, the_file)
        if os.path.isfile(file_path):
            if the_file == ".htaccess":
                continue
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
