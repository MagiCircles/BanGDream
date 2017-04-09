from django.shortcuts import render
from web.utils import getGlobalContext
from web.views import indexExtraContext

def index(request):
    context = getGlobalContext(request)
    indexExtraContext(context)
    return render(request, 'pages/indexBackground.html', context)
