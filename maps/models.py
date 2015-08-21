from django.db import models
from tagging.fields import TagField
from tagging.models import Tag
from django.contrib.auth.models import User
from django.utils import timezone
from django.forms import ModelForm, CharField, Textarea, DateField, ChoiceField, Select, HiddenInput, Form, FileField
import types


# Statements
class Statement( models.Model ) :
	text = models.CharField( max_length=250, unique=True, null=False )
	description = models.TextField( blank=True, null=True )
	user = models.ForeignKey( User, null=False )
	hide = models.BooleanField( default=False ) 
	topics = models.CharField( max_length=250, blank=True, null=True )
	tags = models.CharField( 'Topic', max_length=250, blank=True, null=True )

	def _get_tags(self):
		return Tag.objects.get_for_object(self)
	def _set_tags(self, tags):
		Tag.objects.update_tags(self, tags)
	tags = property(_get_tags, _set_tags)

	def __unicode__( self ) :
		text = self.text
		if len(text) > 60 :
			text = text[0:60] + "..."
		return text

class StatementForm( ModelForm ) :
	tags= CharField( widget=HiddenInput( attrs={'id':"tags"} ), required=False )
	topics = CharField( widget=HiddenInput( attrs={'id':"topics"} ), required=False )

	class Meta :
		model = Statement
		fields = ['text','description', 'user']
		widgets = {
			'text': Textarea( attrs={ 'id':"text", 'rows':2, 'class':"text ui-widget-content ui-corner-all"} ),
			'description': Textarea( attrs={ 'id':"description", 'rows':4, 'class':"text ui-widget-content ui-corner-all" } ),
		}




# Requests for Statements
class StatementRequest( models.Model ) :
	question = models.TextField( blank=True, null=True )
	answer = models.ManyToManyField( Statement, blank=True )

	def __unicode__( self ) :
		return self.question

class StatementRequestForm( ModelForm ) :
	class Meta :
		model = StatementRequest
		fields = ['question','answer']



# Articles
# YEAR_CHOICES = [] 
# for r in range(1900, (datetime.datetime.now().year+1)) : 
# 	YEAR_CHOICES.append((r,r))

class Article( models.Model ) :
	doi = models.CharField( max_length=250, null=True, blank=True )
	title = models.TextField( null=True, blank=True )
	author = models.TextField( null=True, blank=True )
	journal = models.TextField( null=True, blank=True )
	publisher = models.TextField( null=True, blank=True )
	year = models.TextField( null=True, blank=True )
	volume = models.CharField( max_length=10, null=True, blank=True )
	number = models.CharField( max_length=10, null=True, blank=True )
	pages = models.CharField( max_length=20, null=True, blank=True )
	user = models.ForeignKey( User, null=False )
	hide = models.BooleanField( default=False ) 
	annotations = models.CharField( max_length=250, blank=True, null=True )
	tags = models.CharField( 'Annotations', max_length=None, blank=True, null=True )

	def _get_tags(self):
		return Tag.objects.get_for_object(self)
	def _set_tags(self, tags):
		Tag.objects.update_tags(self, tags)
	tags = property(_get_tags, _set_tags)

	def __unicode__( self ) :
		title = self.title
		if len(title) > 60 :
			title = title[0:60] + "..."
		author = self.author
		if len(author) > 20 :
			author = author[0:20] + "..."
		return author + " - " + str(self.year) + " - " + title

class ArticleForm( ModelForm ) :
	tags = CharField( widget=HiddenInput( attrs={'id':"tags"} ), required=False )
	annotations = CharField( widget=HiddenInput( attrs={'id':"annotations"} ), required=False )

	class Meta :
		model = Article
		fields = ['title','author','journal', 'publisher', 'year', 'volume', 'pages', 'number', 'user']
		widgets = {
			'title': Textarea( attrs={ 'id':"title", 'rows':1, 'class':"text ui-widget-content ui-corner-all"} ),
			'author': Textarea( attrs={ 'id':"author", 'rows':1, 'class':"text ui-widget-content ui-corner-all" } ),
			'journal': Textarea( attrs={ 'id':"journal", 'rows':1, 'class':"text ui-widget-content ui-corner-all" } ),
			'publisher': Textarea( attrs={ 'id':"publisher", 'rows':1, 'class':"text ui-widget-content ui-corner-all" } ),
			'year': Textarea( attrs={ 'id':"year", 'rows':1, 'class':"text ui-widget-content ui-corner-all" } ),
		}

class UploadBibTeXForm( Form ):
    file = FileField()




# Evidences
class Evidence( models.Model ) :
	supports = models.ManyToManyField( 'Statement', related_name="evidence_supports_set", blank=True )
	contradicts = models.ManyToManyField( 'Statement', related_name="evidence_contradicts_set", blank=True )
	article = models.ForeignKey( Article, null=True, blank=True )
	file = models.FilePathField( null=True, blank=True )
	name = models.CharField( 'Text', max_length=250 )
	position = models.CharField( max_length=250, null=True, blank=True )
	user = models.ForeignKey( User, null=False )
	hide = models.BooleanField( default=False ) 

	def __unicode__( self ) :
		return self.name
	
class EvidenceForm( ModelForm ) :
	class Meta :
		model = Evidence # to be substitued by Figure and MeasurementForm ... 
		fields = ['supports', 'contradicts', 'article', 'file', 'name', 'position','user']
		widgets = {
			'name': Textarea( attrs={ 'id':"name", 'rows':1, 'class':"text ui-widget-content ui-corner-all"} ),
			'position': Textarea( attrs={ 'id':"position", 'rows':1, 'class':"text ui-widget-content ui-corner-all"} ),
		}



class Figure( Evidence ) :
	#image = ImageField( upload_to='', max_length=250 )
	caption = models.TextField()



class Measurement( Evidence ) :
	unit = models.CharField( max_length=50 )
	# name = models.CharField( max_length=50 )
	value = models.FloatField()
	# pip django JsonField
