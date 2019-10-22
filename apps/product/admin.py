from django.contrib import admin

from product.models import Product, Tag, Taxonomy, Concept, Collection


class CollectionInline(admin.StackedInline):
    model = Collection


class TagInline(admin.TabularInline):
    model = Tag
    raw_id_fields = ['concept']
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ['name', 'desc', 'ref']
    list_display = ('name', 'ref',)
    inlines = [TagInline]


class ConceptInline(admin.TabularInline):
    model = Concept
    raw_id_fields = ['parent']


@admin.register(Taxonomy)
class TaxonomyAdmin(admin.ModelAdmin):
    inlines = [ConceptInline]
