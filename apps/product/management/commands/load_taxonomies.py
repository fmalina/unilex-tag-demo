from django.core.management.base import BaseCommand
from product.models import Taxonomy, Concept
import requests

SOURCE = 'https://unilexicon.com'


def save_children(children, taxonomy, parent):
    """Save children recursively."""
    for child in children:
        c = Concept(
            slug=child['id'],
            name=child['name'],
            taxonomy=taxonomy,
            parent=parent
        )
        c.save()
        save_children(child['children'], taxonomy, c)


def load_uni():
    """Purge and reload FS authority, saving it's taxonomy copies locally"""
    Concept.objects.all().delete()
    Taxonomy.objects.all().delete()

    vocabs = requests.get(SOURCE + '/vocabularies/authority/FS/json').json()

    for vocab in vocabs:
        t = Taxonomy(
            slug=vocab['node_id'],
            name=vocab['name']
        )
        t.save()
        tree = requests.get(SOURCE + vocab['url']).json()

        save_children(tree['children'], t, None)


class Command(BaseCommand):
    def handle(self, *args, **options):
        load_uni()
