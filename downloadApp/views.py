import json
import re
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
        pattern = re.compile('coub\.com\/[\w]+\/[\w]+')
        link_type = request.POST['choice']
        url = request.POST['url_string']
        response = redirect("downloadApp:get_link")

        if link_type == 'Download vkontakte':
            site_id = 1
        elif link_type == 'Download youtube':
            site_id = 2
        elif link_type == 'Download coub':
            site_id = 3
            result = pattern.search(url)
            if result:
                audio_url = find_coub_audio(url)
                if audio_url:
                    response['Location'] += '?' + urllib.urlencode({'url': find_coub_audio(url)})
        else:
            site_id = 0

        return response

    else:
        objList = DownloadRequest.objects.all()
        return render(request, 'index.html', {'test': 'TEST APP', 'list': objList})


def get_link(request):
    url = request.GET.get('url', '')
    if url:
        DownloadRequest(downloaded_url=url, requester_ip='localhost', request_date=timezone.now()).save()
        response = HttpResponse(urllib2.urlopen(url), content_type='audio/mpeg')
        response['Content-Disposition'] = 'attachment; filename="foo.mp3"'
        return response
    else:
        return render(request, 'result.html')

def find_coub_audio(url):
    try:
        htm = lxml.html.parse(url).getroot()
        findArray = [t.text for t in htm.cssselect('script#coubPageCoubJson')]
        js = json.loads(findArray[0])
        return js['audio_versions']['template'].replace('%{version}', 'high')
    except Exception:
        return None


def error404(request):
    return render(request, '404.html')