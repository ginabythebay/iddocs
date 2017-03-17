from django.core.urlresolvers import reverse


def get_build_path(view, name):
    """Return a build path for a name relative to a view.  The view will
       be passed to urlresolvers.reverse() and can be a url pattern name or a
       callable view object."""
    path = reverse(view)
    if path != "":
        path = path[1:]  # strip off leading slash
    return path + name
