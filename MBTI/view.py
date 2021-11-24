from django.shortcuts import render

#
# from django.shortcuts import render_to_response, render


from django.views.generic import View
from django.http import HttpResponse
from django.conf import settings
import os
# from django.shortcuts import render_to_response, render
from django.template import RequestContext
#


def page_not_found_page(request, exception):
    # response = render_to_response('MBTI/templates/404.html',{},context_instance=RequestContext(request))
    # response.status_code=404
    return render(request, '404.html')