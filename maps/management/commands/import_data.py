# ADDITIONAL COMMAND TO IMPORT DATA FROM FILES
# Usage:
# $ python manage.py import_bibtex sample.bib

# LATEX
import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

from maps.models import Article

# CSV TAGS (assuming matching articles ids)
from tagging.models import Tag
import csv
import StringIO


def clean_entry( entry, check ):
    for key in entry.keys():
        if not key in check:
            del entry[key]
    return entry


def handle_bibtex( infile, user=None, verbose=False ):
    if user:
        u = user
    else:
        u = User.objects.get(username='admin')
    # manage data
    # load bibtex file to in-memory db
    parser = BibTexParser()
    parser.customization = convert_to_unicode
    bib_database = bibtexparser.load(infile, parser=parser)
    for art in bib_database.entries:
        if len( Article.objects.filter(title=art['title']) ) == 0:
            art = clean_entry( art, [ 'title', 'author', 'journal', 'publisher', 'year', 'volume', 'pages'] )
            a = Article(user=u, hide=False, **art)
            if verbose:
                print a
            a.save()


def handle_csv( infile, user=None, verbose=False ):
    if user:
        u = user
    else:
        u = User.objects.get(username='admin')
    # manage data
    # load bibtex file to in-memory db
    with open(infile, mode='r') as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            a = Article.objects.get( pk=row['ID'] )
            for tagname in row.keys():
                if tagname not in ['ID','DOI','Title','Author','Year','Annotations']:
                    if row[tagname] != '':
                        Tag.objects.add_tag( a, tagname+":"+row[tagname])




class Command(BaseCommand):
    help = 'Imports a BibTeX formatted list of articles in the KnowledgeBase.'

    def add_arguments(self, parser):
        parser.add_argument('file', nargs='+', type=str)

    def handle(self, *args, **options):
        for filename in options['file']:
            try:
                with open(filename) as bibtex_file:
                    handle_bibtex( bibtex_file, verbose=True )
            except:
                raise CommandError('File "%s" does not exist' % filename)

            self.stdout.write('Successfully uploaded file "%s"' % filename)

