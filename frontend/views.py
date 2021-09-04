from django.shortcuts import render
from django.views.generic import TemplateView


class HomeView(TemplateView):
    """
    メイン画面
    """
    template_name = 'frontend/main.html'


def terms_of_service_view(request):
    """
    利用規約
    """
    return render (request, 'components/terms_of_service.html')


def page_not_found(request, exception):
    """
    404画面
    """
    return render(request, 'components/404.html', status=404)


def server_error(request):
    return render(request, 'components/500.html', status=500)
