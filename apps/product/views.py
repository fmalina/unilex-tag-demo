from django.forms.formsets import formset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from product.forms import TagForm, ProductForm
from product.models import Tag, Product, Concept


class TaggingView(View):
    """For a given piece of content identified by its ID
    GET: request tags & displays returned tags in a compelling interface
    POST: post tags to save user entered tags for a given pk.

    Communicate with local database or proxy remote source using Client.
    """
    template_name = 'product/product.html'
    form = ProductForm

    @staticmethod
    def get_sector(sector_slug):
        filters = Product.SECTOR_FILTERS.copy()
        filters['slug'] = sector_slug
        return Concept.objects.filter(**filters).first()

    @method_decorator(csrf_exempt)
    def post(self, request, pk=None, sector_slug=None):
        product = None

        org = request.user.org_set.first()
        sector = self.get_sector(sector_slug)
        if pk:
            product = Product.objects.get(pk=pk)

        form = self.form(request.POST, instance=product)
        tag_formset = formset_factory(form=TagForm)
        formset = tag_formset(request.POST)

        tags = []
        for tag_form in formset.forms:
            raw_tag = tag_form['predicate'].data
            if raw_tag:
                tag = Concept.objects.get(pk=raw_tag)
                tags.append(tag)
        if form.is_valid():
            d = form.cleaned_data
            d['org'] = org
            d['sector'] = sector
            if not product:
                product = Product(**d)
            product.save()
            for tag in tags:
                _tag, _created = Tag.objects.get_or_create(product=product, concept=tag)
            response = redirect(product.get_absolute_url())
            return response
        return render(request, self.template_name, {
            'product': product,
            'form': form,
            'formset': formset,
            'forms_and_set': zip(formset.forms, tags),
            'base_url': 'https://unilexicon.com'
        })

    def get(self, request, pk=None, sector_slug=None):
        tag_concepts = []
        tag_forms = []
        sector = self.get_sector(sector_slug)
        org = request.user.org_set.first()

        if pk:
            product = get_object_or_404(Product, pk=pk)
            concepts = [tag.concept for tag in product.tag_set.all()]

            for concept in concepts:
                tag_form = {'predicate': concept.id, }
                tag_concepts.append(concept)
                tag_forms.append(tag_form)
        else:
            product = None

        if not tag_concepts:
            tag_concepts = ['addfirst']
        tag_formset = formset_factory(form=TagForm, extra=len(tag_concepts), can_delete=True)
        form = self.form(instance=product, initial={
            'org': org,
            'sector': sector
        })
        formset = tag_formset(initial=tag_forms)
        forms_and_tags = zip(formset.forms, tag_concepts)

        return render(request, self.template_name, {
            'product': product,
            'sector': sector if not product else product.sector,
            'org': org if not product else product.org,
            'form': form,
            'formset': formset,
            'forms_and_set': zip(formset.forms, tag_concepts),
            'base_url': 'https://unilexicon.com'
        })


def products(request):
    org = request.user.org_set.first()
    return render(request, 'product/products.html', {
        'title': 'Your products',
        'products': Product.objects.filter(org=org)
    })


def autocomplete(request):
    """Taxonomy autocomplete"""
    q = request.GET.get('q','').strip()
    concepts = Concept.objects.filter(
        Q(name__icontains=q) |
        Q(slug__istartswith=q)
    )
    response = render(request, 'product/autocomplete.txt', {'concepts': concepts})
    response['Access-Control-Allow-Origin'] = '*'
    return response
