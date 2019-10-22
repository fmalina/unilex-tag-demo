from org.models import Org, OrgUser
from django.contrib import admin
from product.admin import CollectionInline


class OrgUserInline(admin.StackedInline):
    model = OrgUser
    raw_id_fields = ('user',)
    extra = 0


class OrgAdmin(admin.ModelAdmin):
    search_fields = ['name', 'postcode']
    list_display = 'name postcode updated_at'.split()
    exclude = ('coords',)
    inlines = [OrgUserInline, CollectionInline]


class OrgUserAdmin(admin.ModelAdmin):
    raw_id_fields = ('user', 'org')
    list_display = ['org', 'user', 'created_at', 'updated_at']


admin.site.register(Org, OrgAdmin)
admin.site.register(OrgUser, OrgUserAdmin)
