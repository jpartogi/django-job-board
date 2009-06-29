from datetime import datetime

from django.db import models
from django.contrib import admin

from portal.apps.jobs.models import Job

class JobAdmin(admin.ModelAdmin):
    date_hierarchy = 'posted'
    search_fields = ['title', 'description']
    list_display = ['title', 'job_type', 'skills_required', 'location', 'company_name', 'onsite_required', 'posted']
    list_filter = ['posted', 'job_type', 'location', 'onsite_required']
    fieldsets = (
        ('Job Information', {
            'fields': ('title','job_type', 'description', 'skills_required', ('location', 'onsite_required')),
        }),
        ('Company Information', {
            'fields': ('company_name', ('contact_person', 'contact_email'), 'website', 'budget'),
        }),
    )

    def save_model(self, request, obj, form, change):
        obj.posted = datetime.now()
        obj.save()
        
admin.site.register(Job, JobAdmin)