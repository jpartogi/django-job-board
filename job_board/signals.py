import django.dispatch

view_job = django.dispatch.Signal(providing_args=["job"])