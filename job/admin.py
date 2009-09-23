from django.contrib import admin

from job.models import Job

class JobAdmin(admin.ModelAdmin):
    date_hierarchy = 'posted'
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ['title', 'description']
    list_display = ['title', 'job_type', 'skills_required', 'location', 'company_name', 'onsite_required', 'posted']
    list_filter = ['posted', 'job_type', 'location', 'onsite_required']
    fieldsets = (
        ('Job Information', {
            'fields': ('title', 'slug', 'job_type', 'description', 'skills_required', ('location', 'onsite_required')),
        }),
        ('Company Information', {
            'fields': ('company_name', ('contact_person', 'contact_email'), 'website', 'budget'),
        }),
    )
        
admin.site.register(Job, JobAdmin)