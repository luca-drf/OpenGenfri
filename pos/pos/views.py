from django.http import HttpResponse
from webpos.models import Category

def check(request):
    try:
        qs = Category.objects.all()
        list(qs)
        return HttpResponse("OK")
    except Exception:
        return HttpResponse("NO")
