import datetime
import re
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.db.models import Q, Count
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django_comments.views.comments import post_comment
from django.core.context_processors import csrf
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from django.template import Context, RequestContext, loader

from tagging.models import Tag

from maps.models import StatementRequest
from maps.models import Statement
from maps.models import Article
from maps.models import Evidence
from maps.models import Figure
from maps.models import Measurement
from maps.models import StatementRequestForm
from maps.models import StatementForm
from maps.models import EvidenceForm
from maps.models import ArticleForm

from maps.models import UploadBibTeXForm
from maps.management.commands.import_bibtex import handle_bibtex



def home(request, template):
    """Return the homepage of the website."""
    response = render_to_response(template, RequestContext(request, {'user':request.user}))
    return response

def project_url(request):
    return "fake url"


# REQUESTS FOR STATEMENTS

@login_required
def stmt_requests( request ) :
	user = request.user
	request_list = StatementRequest.objects.annotate( answer_count=Count('answer__id') )
   	# output
   	t = loader.get_template( 'requests.html' )
   	c = Context( {
	'user': user,
   	        'request_list': request_list,
   	} )
   	c.update(csrf(request))
   	return HttpResponse( t.render( c ) )


# OPERATIONS ON CARDS

@login_required
def stmt_requests_add( request ) :
	user = request.user
	res = ValueError
	ntt_id = int( request.GET.get('ntt_id', 0) )
	form = StatementRequestForm( auto_id=False )
	if ntt_id > 0 :
		s = StatementRequest.objects.get( pk=ntt_id )
		form = StatementRequestForm( request.GET, instance=s )
		res = form.save()
	else :
		form = StatementRequestForm( request.GET )
		res = form.save()
	# feedback
	if res != ValueError :
		return HttpResponse( "Request successfully saved" )
	else :
		return HttpResponse( res )


@login_required
def stmt_requests_edit( request ) :
	ntt_id = int( request.GET.get('ntt_id', 0) )
	form = StatementRequestForm( auto_id=False )
	formtempl = "request_form.html"
	if ntt_id > 0 :
		s = StatementRequest.objects.get( pk=ntt_id )
		form = StatementRequestForm( instance=s )
	# create form html
	template_vars = RequestContext( request, { 'form':form } )
	return render_to_response( formtempl, template_vars )



@login_required
def add( request ) :
	user = request.user
	res = ValueError
	entity = request.GET.get('entity', "")
	ntt_id = int( request.GET.get('ntt_id', 0) )
	print ntt_id
	if entity == 'stmt' :
		form = StatementForm( auto_id=False )
		if ntt_id > 0 :
			s = Statement.objects.get( pk=ntt_id )
			form = StatementForm( request.GET, instance=s )
			res = form.save()
			s.tags = form.cleaned_data['tags']
			s.topics = ', '.join(s.tags.values_list('name',flat=True) )
			s.save()
		else :
			form = StatementForm( request.GET )
			res = form.save()
			s = Statement.objects.get( text=form.cleaned_data['text'] )
			s.tags = form.cleaned_data['tags']
			s.topics = ', '.join(s.tags.values_list('name',flat=True) )
			res = s.save()
	elif entity == 'evdc' :
		form = EvidenceForm( auto_id=False, initial={'supports':0,'contradicts':0} )
		if ntt_id > 0 :
			e = Evidence.objects.get( pk=ntt_id )
			form = EvidenceForm( request.GET, instance=e, initial={'supports':[],'contradicts':[]} )
			res = form.save()
		else :
			form = EvidenceForm( request.GET, initial={'supports':[],'contradicts':[]} )
			res = form.save()
	elif entity == 'artl' :
		form = ArticleForm( auto_id=False )
		if ntt_id > 0 :
			a = Article.objects.get( pk=ntt_id )
			form = ArticleForm( request.GET, instance=a )
			res = form.save()
		else :
			form = ArticleForm( request.GET )
			res = form.save()
	# feedback
	if res != ValueError :
		return HttpResponse( "Record successfully saved" )
	else :
		return HttpResponse( res )



@login_required
def edit( request ) :
	if not request.user.is_authenticated() :
    		return HttpResponse( "You need to be logged in to do this..." )
	user = request.user
	entity = request.GET.get('entity', "")
	ntt_id = int( request.GET.get('ntt_id', 0) )
	topic = ''
	topic_list = []
	# Entity type switch
	if entity == 'stmt' :
		form = StatementForm( auto_id=False )
		formtempl = "stmt_form.html"
		if ntt_id > 0 :
			s = Statement.objects.get( pk=ntt_id )
			if len(s.tags) > 0 :
				topic_list = s.tags.values_list('name',flat=True)
				topic = ', '.join( topic_list )
			form = StatementForm( instance=s, initial={'tags':topic} )
	elif entity == 'evdc' :
		form = EvidenceForm( auto_id=False )
		formtempl = "evdc_form.html"
		if ntt_id > 0 :
			e = Evidence.objects.get( pk=ntt_id )
			form = EvidenceForm( instance=e )
	elif entity == 'artl' :
		form = ArticleForm( auto_id=False )
		formtempl = "artl_form.html"
		if ntt_id > 0 :
			a = Article.objects.get( pk=ntt_id )
			form = ArticleForm( instance=a )
	# create form html
	template_vars = RequestContext( request, { 'form':form, 'user':user, 'topics':topic, 'topic_list':topic_list } )
	return render_to_response( formtempl, template_vars )



@login_required
def delete( request ) :
	if not request.user.is_authenticated() :
    		return HttpResponse( "You need to be logged in to do this..." )
	user = request.user
	entity = request.GET.get('entity', "")
	ntt_id = request.GET.get('ntt_id', 0)
	# choose deletion object
	if entity == 'stmt' :
		s = Statement.objects.get( pk=ntt_id )
		s.hide = True
		s.save()
	elif entity == 'evdc' :
		e = Evidence.objects.get( pk=ntt_id )
		e.hide = True
		e.save()
	elif entity == 'artl' :
		a = Article.objects.get( pk=ntt_id )
		a.hide = True
		a.save()
	return HttpResponse( "Record %s removed" % ntt_id )



# FILTER AND HIGHLIGHT CARDS

def setSession( request ) :
	request.session.set_test_cookie()
	if request.session.test_cookie_worked():
		request.session.delete_test_cookie()
	else:
		return False
	# FILTER
	request.session['filter_stmt'] = ""
	request.session['clean_stmt'] = "false"
	request.session['filter_evdc'] = ""
	request.session['clean_evdc'] = "false"
	request.session['filter_artl'] = ""
	request.session['clean_artl'] = "false"
	return True


@csrf_protect
def getFilters( request ) :
	# Session check
	if not 'filter_stmt' in request.session :
		if not setSession( request ) :
			return False
	# GET FILTERS: if post or session have filtering options
	# STMT
	if 'clean_stmt' in request.POST :
		request.session['filter_stmt'] = ""
		request.session['clean_stmt'] = 'false'
	# query string
	stmt_string = ""
	if ('filter_stmt' in request.session) and request.session['filter_stmt']!="" :
		stmt_string = request.session['filter_stmt']
	if 'filter_stmt' in request.POST :
		stmt_string = request.POST.get('filter_stmt', "").strip()
		request.session['filter_stmt'] = stmt_string
	# filtered ids
	filtered_stmt_ids = []
	if stmt_string != "" :
       		entry_query = get_query( stmt_string, ['text','topics',] )
       		stmt_list = Statement.objects.filter( entry_query )
		for s in stmt_list :
			filtered_stmt_ids.append( s.id )
	# EVDC
	if 'clean_evdc' in request.POST :
		request.session['filter_evdc'] = ""
		request.session['clean_evdc'] = 'false'
	# query string
	evdc_string = ""
	if ('filter_evdc' in request.session) and request.session['filter_evdc']!="" :
		evdc_string = request.session['filter_evdc']
	if 'filter_evdc' in request.POST :
		evdc_string = request.POST.get('filter_evdc', "").strip()
		request.session['filter_evdc'] = evdc_string
	# filtered ids
	filtered_evdc_ids = []
	if evdc_string != "" :
       		entry_query = get_query( evdc_string, ['name',] )
       		evdc_list = Evidence.objects.filter( entry_query )
		for e in evdc_list :
			filtered_evdc_ids.append( e.id )
	# ARTL
	if 'clean_artl' in request.POST :
		request.session['filter_artl'] = ""
		request.session['clean_artl'] = 'false'
	# query string
	artl_string = ""
	if ('filter_artl' in request.session) and request.session['filter_artl']!="" :
		artl_string = request.session['filter_artl']
	if 'filter_artl' in request.POST :
		artl_string = request.POST.get('filter_artl', "").strip()
		request.session['filter_artl'] = artl_string
	# filtered ids
	filtered_artl_ids = []
	if artl_string != "" :
       		entry_query = get_query( artl_string, ['title','author'] )
       		artl_list = Article.objects.filter( entry_query )
		for a in artl_list :
			filtered_artl_ids.append( a.id )
	# output
	return { 
		'stmt':stmt_string, 
		'stmt_ids':filtered_stmt_ids, 
		'evdc':evdc_string, 
		'evdc_ids':filtered_evdc_ids, 
		'artl':artl_string, 
		'artl_ids':filtered_artl_ids, 
	}


@login_required
@csrf_protect
def map( request ) :
	user = request.user
	# FILTERS
	filters = getFilters( request )
	if filters :
		# STATEMENTS 
		stmt_list = getStatements( request, [0], filters, 'map' )
		# EVIDENCE
		evidence_list = getEvidence( request, [0], filters, 'map' )
		# ARTICLES
		article_list = getArticles( request, [0], filters, 'map' ) 
	else :
		stmt_list = []
		evidence_list = []
		article_list = []
		filters['stmt'] = ''
		filters['evdc'] = ''
		filters['artl'] = ''
   	# output
   	t = loader.get_template( 'map.html' )
   	c = Context( {
		'user': user,
		'stmt_list': stmt_list,
		'article_list': article_list,
		'evidence_list': evidence_list,
		'filter_stmt': filters['stmt'],
		'filter_evdc': filters['evdc'],
		'filter_artl': filters['artl'],
   	} )
   	c.update(csrf(request))
   	# return HttpResponse( t.render( c ) )
   	return render(request, 'map.html', c)

		



def getStatements( request, ref, filters, setFrom ) :
	# create color-ed list
	obj_list = Statement.objects.exclude(hide=True)
	if isinstance( ref, list ) : #else :
		obj_list = Statement.objects.exclude(hide=True).extra( 
			select={ 'color': "CASE WHEN (id in (0"+ ','.join(str(r) for r in ref) +")) THEN 'Yellow' ELSE 'Zone' END" } 
			).order_by('color')
	else :
		obj_list = Statement.objects.exclude(hide=True).extra( 
			select={ 'color': "CASE WHEN id="+str(ref)+" THEN 'Yellow' ELSE 'Zone' END" } 
			).order_by('color')
	# apply filters
	filtered_stmt_ids = []
	if len(filters['evdc_ids']) > 0 :
		evdc_stmt = Evidence.objects.filter( id__in=filters['evdc_ids'] ).exclude(hide=True)
		for e in evdc_stmt :
			filtered_stmt_ids.extend( e.supports.values_list('id',flat=True) )
			filtered_stmt_ids.extend( e.contradicts.values_list('id',flat=True) )
	if len(filters['artl_ids']) > 0 :
		evdc_stmt = Evidence.objects.filter( article__in=filters['artl_ids'] ).exclude(hide=True)
		for e in evdc_stmt :
			filtered_stmt_ids.extend( e.supports.values_list('id',flat=True) )
	# assign filter even if not present, but due to filters on other entities
	if len(filters['stmt_ids']) > 0 and len(filtered_stmt_ids)>0 :
		filters['stmt_ids'] = list( set(filtered_stmt_ids) & set(filters['stmt_ids']) ) # intersect
	elif len(filtered_stmt_ids) > 0 :
		filters['stmt_ids'] = filtered_stmt_ids 
	# even after all, there can be no filters so check
	if len(filters['stmt_ids']) > 0 :
		obj_list = obj_list.filter( id__in = filters['stmt_ids'] )
	# output
	return obj_list


def getEvidence( request, ref, filters, setFrom ) :
	# create color-ed list
	if setFrom == 'evdc' or setFrom=='artl' or setFrom=='map' :
		if isinstance( ref, list ) : # int
			clause = "CASE WHEN id in (0,"+ ','.join(str(s) for s in ref)+") THEN 'Yellow' ELSE 'Zone' END" 
		else : # artl
			clause = "CASE WHEN id="+str(ref)+" THEN 'Yellow' ELSE 'Zone' END" 
		obj_list = Evidence.objects.exclude(hide=True).extra( select={'color':clause} ).order_by('color')
	if setFrom=='stmt' :
		evdc_supports = []
		evdc_contra = []
		if isinstance( ref, int ) :
			evdc_supports = Evidence.objects.filter( supports__id=ref ).exclude(hide=True).values_list('id',flat=True)
			evdc_contra = Evidence.objects.filter( contradicts__id=ref ).exclude(hide=True).values_list('id',flat=True)
		else :
			evdc_supports = Evidence.objects.filter( supports__id__in=ref ).exclude(hide=True).values_list('id',flat=True)
			evdc_contra = Evidence.objects.filter( contradicts__id__in=ref ).exclude(hide=True).values_list('id',flat=True)
		# colouring
		clause = "CASE WHEN id in (0"+ ','.join(str(s) for s in evdc_supports) +") THEN 'Yellow' WHEN id in (0"+ ','.join(str(c) for c in evdc_contra)+") THEN 'Red' ELSE 'Zone' END" 
		obj_list = Evidence.objects.exclude(hide=True).extra( select={'color':clause} ).order_by('color')
	# filters
	filtered_evdc_ids = []
	if len(filters['stmt_ids']) > 0 :
		evdc_supports_stmt = Evidence.objects.filter( supports__id__in=filters['stmt_ids'] ).exclude(hide=True)
		for e in evdc_supports_stmt :
			filtered_evdc_ids.append( e.id )
		evdc_contra_stmt = Evidence.objects.filter( contradicts__id__in=filters['stmt_ids'] ).exclude(hide=True)
		for e in evdc_contra_stmt :
			filtered_evdc_ids.append( e.id )
	if len(filters['artl_ids']) > 0 :
		evdc_artl = Evidence.objects.filter( article__in=filters['artl_ids'] ).exclude(hide=True)
		for e in evdc_artl :
			filtered_evdc_ids.append( e.id )
	# assign filter even if not present, but due to filters on other entities
	if len(filters['evdc_ids']) > 0 :
		filters['evdc_ids'] = list( set(filtered_evdc_ids) & set(filters['evdc_ids']) ) # intersect
	elif len(filtered_evdc_ids) > 0 :
		filters['evdc_ids'] = filtered_evdc_ids 
	# even after all, there can be no filters so check
	if len(filters['evdc_ids']) > 0 :
		obj_list = obj_list.filter( id__in = filters['evdc_ids'] )
	# output
	return obj_list


def getArticles( request, ref, filters, setFrom ) :
	obj_list = Article.objects.exclude(hide=True)
	if isinstance( ref, list ) :
		obj_list = Article.objects.exclude(hide=True).extra( 
			select={ 'color': "CASE WHEN id in (0"+ ','.join(str(r) for r in ref) +") THEN 'Yellow' ELSE 'Zone' END" } 
			).order_by('color')
	else :
		obj_list = Article.objects.exclude(hide=True).extra( 
			select={ 'color': "CASE WHEN id="+str(ref)+" THEN 'Yellow' ELSE 'Zone' END" } 
			).order_by('color')
	# filters
	filtered_artl_ids = []
	if len(filters['stmt_ids']) > 0 :
		evdc_stmt = Evidence.objects.filter( supports__id__in=filters['stmt_ids'] ).exclude(hide=True)
		for e in evdc_stmt :
			filtered_artl_ids.append( e.article.id )
	if len(filters['evdc_ids']) > 0 :
		evdc_artl = Evidence.objects.filter( article__in=filters['artl_ids'] ).exclude(hide=True)
		for e in evdc_artl :
			filtered_artl_ids.append( e.article.id )
	# assign filter even if not present, but due to filters on other entities
	if len(filters['artl_ids']) > 0 :
		filters['artl_ids'] = list( set(filtered_artl_ids) & set(filters['artl_ids']) ) # intersect
	elif len(filtered_artl_ids) > 0 :
		filters['artl_ids'] = filtered_artl_ids 
	# even after all, there can be no filters so check
	if len(filters['artl_ids']) > 0 :
		obj_list = obj_list.filter( id__in = filters['artl_ids'] )
	# output
	return obj_list



@login_required
@csrf_protect
def highlight_stmt( request, stmt_id ) :
	stmt_id = int( stmt_id )
	user = request.user
	# FILTERS
	filters = getFilters( request )
	# STATEMENTS 
	stmt_list = getStatements( request, stmt_id, filters, 'stmt' )
	# EVIDENCE
	evidence_list = getEvidence( request, stmt_id, filters, 'stmt' )
	# ARTICLES
	evidence_list_stmt = list(Evidence.objects.exclude(hide=True).filter( supports__id=stmt_id ).values_list('id',flat=True))
	article_list_evdc = list(Article.objects.exclude(hide=True).filter( id__in=Evidence.objects.filter( id__in=evidence_list_stmt ).values_list('article',flat=True) ).values_list('id',flat=True))
	article_list = getArticles( request, article_list_evdc, filters, 'stmt' ) 
	# output
	t = loader.get_template( 'map.html' )
	c = Context( {
		'user': user,
		'stmt_id': stmt_id,
		'stmt_list': stmt_list,
		'evidence_list': evidence_list,
		'article_list': article_list,
		'filter_stmt': filters['stmt'],
		'filter_evdc': filters['evdc'],
		'filter_artl': filters['artl'],
	} )
	c.update(csrf(request))
	return HttpResponse( t.render( c ) )



@login_required
@csrf_protect
def highlight_evdc( request, evdc_id ) :
	user = request.user
	# FILTERS
	filters = getFilters( request )
	# STATEMENT
	stmt_list_evdc = []
	stmt_list_evdc = list(Evidence.objects.exclude(hide=True).get( pk=evdc_id ).supports.all().values_list('id',flat=True)) 
	stmt_list = getStatements( request, stmt_list_evdc, filters, 'evdc' ) 
	# EVIDENCE
	evidence_list = getEvidence( request, evdc_id, filters, 'evdc' )
	# ARTICLE
	artl = Evidence.objects.get(pk=evdc_id).article
	if artl is None :
		artl_id = 0
	else :
		artl_id = artl.id
	article_list = getArticles( request, artl_id, filters, 'evdc' )
	# output
	t = loader.get_template( 'map.html' )
	c = Context( {
		'user': user,
		'evdc_id': evdc_id,
		'stmt_list': stmt_list,
		'evidence_list': evidence_list,
		'article_list': article_list,
		'filter_stmt': filters['stmt'],
		'filter_evdc': filters['evdc'],
		'filter_artl': filters['artl'],
	} )
	c.update(csrf(request))
	return HttpResponse( t.render( c ) )



@login_required
@csrf_protect
def highlight_artl( request, artl_id ) :
	user = request.user
	# FILTERS
	filters = getFilters( request )
	# ID lists
	evdc_list_artl = Evidence.objects.filter( article=artl_id ).exclude(hide=True)
	stmt_list_evdc = []
	list_evdc = [0] # it is possible to have articles not linked to any evidence
	list_evdc.extend( list(evdc_list_artl.values_list('id',flat=True)) )
	for e in evdc_list_artl :
		stmt_list_evdc.extend( e.supports.values_list('id',flat=True) )
	# STATEMENT
	stmt_list = getStatements( request, stmt_list_evdc, filters, 'artl' ) 
	# EVIDENCE
	evidence_list = getEvidence( request, list_evdc, filters, 'artl' )
	# ARTICLE
	article_list = getArticles( request, artl_id, filters, 'artl' )
	# output
	t = loader.get_template( 'map.html' )
	c = Context( {
		'user': user,
		'stmt_list': stmt_list,
		'evidence_list': evidence_list,
		'article_list': article_list,
		'filter_stmt': filters['stmt'],
		'filter_evdc': filters['evdc'],
		'filter_artl': filters['artl'],
	} )
	c.update(csrf(request))
	return HttpResponse( t.render( c ) )



@login_required
def detail( request, entity, ntt_id ) :
	user = request.user
	if entity == 'statement' :
		template = "stmt_detail.html"
		record = Statement.objects.get( pk=ntt_id )
	elif entity == 'evidence' :
		template = "evdc_detail.html"
		record = Evidence.objects.get( pk=ntt_id )
	elif entity == 'article' :
		template = "artl_detail.html"
		record = Article.objects.get( pk=ntt_id )
	# output
	t = loader.get_template( 'detail.html' )
	c = Context( {
		'user': user,
		'entity': entity,
		'ntt_id': ntt_id,
		'detail_template': template,
		'record': record,
	} )
	c.update(csrf(request))
	return HttpResponse( t.render( c ) )



@login_required
@csrf_protect
def upload_bibtex(request):
	user = request.user
	# file handling
	if request.method == 'POST':
		form = UploadBibTeXForm( request.POST, request.FILES )
		if form.is_valid():
			print request.FILES['file']
			handle_bibtex( request.FILES['file'], user=user )
			return HttpResponseRedirect( '/knowledgebase/map/' )
	else:
			form = UploadBibTeXForm()
	# render
	t = loader.get_template( 'upload.html' )
	c = Context( {
		'user': user,
		'form': form,
	} )
	c.update(csrf(request))
	return HttpResponse( t.render( c ) )



def home( request ) :
	if request.user.is_authenticated():
		return HttpResponseRedirect('/knowledgebase/questions/')
	return HttpResponseRedirect('/knowledgebase/login/')



def logout_page( request ) :
	logout(request)
	return HttpResponseRedirect('/knowledgebase/login/')



def help( request ) :
	return render_to_response( 'help.html', {'user': request.user} )



#@csrf_exempt
def comment_post_wrapper( request ):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/knowledgebase/login/')
	post_comment( request )
	# redirecting to the same item
	entity = request.POST.get('content_type', "statement").replace('maps.','')
	ntt_id = int( request.POST.get('object_pk', 8) )
	return HttpResponseRedirect( '/knowledgebase/map/' + entity + '/' + str(ntt_id) )


# SEARCH
def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:
        
        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    
    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)] 

def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.
    '''
    query = None # Query to search for every search term        
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query | or_query
    return query
