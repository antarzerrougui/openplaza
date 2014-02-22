from django.contrib.sites.admin import SiteAdmin

SiteAdmin.list_display += ('code','api','key','secret','is_active')
SiteAdmin.list_filter += ('code','api','key','secret','is_active')