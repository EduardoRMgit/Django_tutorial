from django.shortcuts import render


def web_chat(request):
    return render(request, 'servicios/webchat.html')
