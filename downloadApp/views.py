import json
import urllib
import urllib2
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
# Create your views here.
import lxml.html
import sys
from django.utils import timezone
from django.utils.encoding import smart_str
from models import DownloadRequest


def index(request):
    if request.method == 'POST':
        link_type = request.POST['choice']
        url = request.POST['url_string']
        if link_type == 'Download vkontakte':
           site_id = 1
        elif link_type == 'Download youtube':
           site_id = 2
        elif link_type == 'Download coub':
           site_id = 3
        else:
            site_id = 0
            # pResponseRedirect(reverse('getting_started_info', kwargs={'location': location}))url
        # sys.stdout.write(urllib.urlencode({'?url':find_coub_audio(url)}))
        # sys.stdout.write(urllib.urlencode({'url':find_coub_audio(url)}))
        # sys.stdout.write(urllib.quote(find_coub_audio(url)))
        response = redirect("downloadApp:get_link")
        response['Location']+='?'+urllib.urlencode({'url':find_coub_audio(url)})
        return response
        # response['Location'] += '?your=querystring'
        # return response
        # return HttpResponseRedirect(reverse("downloadApp:get_link", kwargs={'url': url}))
        # return "%s?url=%s" % (redirect("downloadApp:get_link"), urllib.urlencode(url))
    else:
       objList = DownloadRequest.objects.all()
       return render(request,'index.html',{'test': 'TEST APP','list' : objList})

def get_link(request):
    url = request.GET['url']
    DownloadRequest(downloaded_url=url, requester_ip='localhost', request_date=timezone.now()).save()
    response = HttpResponse(urllib2.urlopen(url), content_type='audio/mpeg')
    response['Content-Disposition'] = 'attachment; filename="foo.mp3"'
    return response

    # path_to_file = url
    # response = HttpResponse(mimetype='application/force-download')
    # response['Content-Disposition'] = 'attachment; filename=Audio.mp3'
    # response['X-Sendfile'] = smart_str(path_to_file)
    # return HttpResponse(url,mimetype='audio/mpeg')
    # return render(request, 'result.html', {'url_link':url})

def find_coub_audio(url):
    htm = lxml.html.parse(url).getroot()
    findArray = [t.text for t in htm.cssselect('script#coubPageCoubJson')]
    js = json.loads(findArray[0])
    return js['audio_versions']['template'].replace('%{version}','high')

def error404(request):
    return render(request,'404.html')