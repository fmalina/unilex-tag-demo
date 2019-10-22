from datetime import datetime
from django.db import models
from django.urls import reverse


def weeks(no):
    return [(1, '1 week')] + [(x, f'{x} weeks') for x in range(2, no + 1)]


class Product(models.Model):
    SECTOR_FILTERS = {'taxonomy__slug': 'fs', 'parent__slug': 'sector'}

    name = models.CharField('Product name', max_length=150)
    desc = models.TextField(verbose_name="Description")
    ref = models.CharField(max_length=80, verbose_name="Unique product reference")
    price_range = models.CharField('Price range (briefly)', max_length=80)

    org = models.ForeignKey(
        'org.Org', verbose_name='Supplier organisation',
        on_delete=models.PROTECT
    )
    sector = models.ForeignKey(
        'product.Concept',
        verbose_name='Sector',
        limit_choices_to=SECTOR_FILTERS,
        on_delete=models.PROTECT
    )
    collection = models.ForeignKey(
        'product.Collection',
        verbose_name='Collection',
        blank=True, null=True,
        on_delete=models.SET_NULL
    )
    ethical = models.BooleanField(verbose_name="Ethical product", default=False)
    stock_service = models.BooleanField(default=False)
    small_quantities = models.BooleanField(default=False)
    supply_ability = models.IntegerField(blank=True, null=True)
    moq = models.IntegerField(verbose_name='Minimum Order Quantity', default=0)
    lead_time_sampling = models.IntegerField(
        verbose_name='Lead Time for Sampling',
        choices=weeks(4), default=4
    )
    lead_time_production = models.IntegerField(
        verbose_name='Lead Time for Production',
        choices=weeks(12), default=8
    )

    size_w = models.IntegerField(verbose_name='Width (mm)', null=True, blank=True)
    size_h = models.IntegerField(verbose_name='Height', null=True, blank=True)
    size_d = models.IntegerField(verbose_name='Depth', null=True, blank=True)

    updated_at = models.DateTimeField(default=datetime.now, editable=False)
    created_at = models.DateTimeField(default=datetime.now, editable=False)

    def get_absolute_url(self):
        return reverse('product', args=[self.pk])

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()
        super(Product, self).save(*args, **kwargs)

    class Meta:
        pass
        # unique_together = ['ref', 'org']


class Collection(models.Model):
    org = models.ForeignKey('org.Org', on_delete=models.CASCADE)
    name = models.CharField(max_length=85)


class Tag(models.Model):
    """Tags linking concepts to product."""
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    concept = models.ForeignKey('product.Concept', on_delete=models.CASCADE)

    updated_at = models.DateTimeField(default=datetime.now, editable=False)
    created_at = models.DateTimeField(default=datetime.now, editable=False)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()
        super(Tag, self).save(*args, **kwargs)


class Taxonomy(models.Model):
    slug = models.SlugField(max_length=80, primary_key=True)
    name = models.CharField(max_length=80)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = 'Taxonomies'


class Concept(models.Model):
    slug = models.SlugField(max_length=80, primary_key=True)
    name = models.CharField(max_length=80)
    taxonomy = models.ForeignKey('product.Taxonomy', on_delete=models.PROTECT)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        """Listings for this concept."""
        # TODO not implemented yet
        return self.slug

    def _recurse_for_parents(self, o):
        ls = []
        if o:
            parent = o.parent
            ls.append(parent)
            if parent != self:
                ls += self._recurse_for_parents(parent)
        if o == self and ls:
            ls.reverse()
        return ls

    def breadcrumb(self):
        ls = self._recurse_for_parents(self)
        ls.pop(0)
        return [self.taxonomy] + ls + [self]

    def get_path(self):
        return [x.name for x in self.breadcrumb()]

    def backwards_path(self):
        p = self.get_path()
        p.reverse()
        return ' « '.join(p)

    @property
    def count(self):
        """Number of products with this concept."""
        # TODO not implemented yet
        return 0

    class Meta:
        unique_together = ['slug', 'taxonomy']
