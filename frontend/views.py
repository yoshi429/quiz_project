from django.shortcuts import render
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'frontend/main.html'


def terms_of_service_view(request):
    return render (request, 'components/terms_of_service.html')

def page_not_found(request, exception):
    return render(request, 'components/404.html', status=404)


def server_error(request):
    return render(request, 'components/500.html', status=500)
