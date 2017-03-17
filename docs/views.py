from bakery.views import BuildableTemplateView

class IndexView(BuildableTemplateView):
    template_name = 'docs/index.html'
    build_path = 'index.html'

