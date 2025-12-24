from django.shortcuts import render


def about(request):
    """Страница о проекте."""
    return render(request, 'pages/about.html')


def rules(request):
    """Страница с правилами."""
    return render(request, 'pages/rules.html')
