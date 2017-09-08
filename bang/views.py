from django.shortcuts import render
from magi.utils import getGlobalContext
from magi.views import indexExtraContext

def index(request):
    context = getGlobalContext(request)
    indexExtraContext(context)
    return render(request, 'pages/indexBackground.html', context)
