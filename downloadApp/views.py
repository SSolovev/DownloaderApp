from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
# Create your views here.


def index(request):
    return render(request,'index.html',{'test': 'TEST APP'})

def get_link(request):
    link = request.POST['url_string']
    link_type = request.POST['choice']
    if link_type == 'Download vkontakte':
        res='vk'
    elif link_type == 'Download youtube':
        res='youtube'
    elif link_type == 'Download coub':
        res = 'coub'
    return render(request, 'result.html', {'res':res})
    return HttpResponseRedirect(reverse("downloadApp:res", args=(res,)))

# def res(re)