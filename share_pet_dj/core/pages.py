from django.views.generic import TemplateView


class Handler500View(TemplateView):
    template_name = 'core/500.html'


class Handler404View(TemplateView):
    template_name = 'core/404.html'


class Handler400View(TemplateView):
    template_name = 'core/400.html'


handler500 = Handler500View.as_view()
handler404 = Handler404View.as_view()
handler400 = Handler400View.as_view()
