from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.urlresolvers import reverse

from recaptcha.client import captcha

from job.models import *
from job.forms import *

#TODO: Add form preview before submitting
def add(request):
    html_captcha = captcha.displayhtml(settings.RECAPTCHA_PUB_KEY)
    
    if request.method == 'POST':
        
        check_captcha = captcha.submit(request.POST['recaptcha_challenge_field'], 
                                       request.POST['recaptcha_response_field'],
                                       settings.RECAPTCHA_PRIVATE_KEY,
                                       request.META['SERVER_NAME'])
        
	if check_captcha.is_valid is False:
            # Captcha is wrong show an error ...
            request.notifications.create('Captcha challenge is wrong.', 'error')
            
            return HttpResponseRedirect(reverse('job-form'))
        
        form = JobForm(request.POST)

        if form.is_valid():
            job = form.save()
            request.notifications.create('Your job posting has been saved successfully.', 'success')

            return HttpResponseRedirect(reverse('job-list')) # Redirect after POST

    else:
        form = JobForm()
   
    return render_to_response('job/form.html', {
        'request': request,
        'form': form,
        'html_captcha': html_captcha,
    }, context_instance=RequestContext(request))