from django.contrib import admin

from job_board.models import Job, JobCategory

class JobCategoryAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'description', 'slug')
    
class JobAdmin(admin.ModelAdmin):
    date_hierarchy = 'posted'
    search_fields = ['title', 'description']
    list_display = ['title', 'job_type', 'category', 'location',
                    'company_name', 'onsite_required', 'posted', 'viewed']
    list_filter = ['posted', 'job_type', 'category', 'onsite_required']
    fieldsets = (
        ('Job Information', {
            'fields': ('title', 'slug', 'job_type', 'category', 'description', ('location', 'onsite_required')),
        }),
        ('Company Information', {
            'fields': ('company_name', ('to_apply'), 'website'),
        }),
    )
        
admin.site.register(Job, JobAdmin)
admin.site.register(JobCategory, JobCategoryAdmin)