from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def get_admin_app_list(context):
    from django.contrib import admin
    return admin.site.get_app_list(context['request'])