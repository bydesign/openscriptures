from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.http import Http404
from django.template import RequestContext
from core.models import Ref, Token, Work, TokenParsing
import logging

def index(request):
    return HttpResponse("Hello, world. This is the index.")
   
def viewer(request):
	return render_to_response('work_viewer.html', {
		'works': Work.objects.all(),
	})

def ajaxTok(request, work_slug, ref_slug, ref_slug_end=None):
	#ref_start = get_object_or_404(Ref, work__osis_slug=work_slug, osis_id=ref_slug)
	try: ref_start = Ref.objects.select_related('start_token', 'end_token').get(work__osis_slug=work_slug, osis_id=ref_slug)
	except: raise Http404
	ref_end = None
	if ref_slug_end:
		#ref_end = get_object_or_404(Ref, work__osis_slug=work_slug, osis_id=ref_slug_end)
		try: ref_end = Ref.objects.select_related('start_token', 'end_token').get(work__osis_slug=work_slug, osis_id=ref_slug_end)
		except: raise Http404
		
	return ajaxSlugs(request, work_slug, ref_start, ref_end)

def ajaxTokSimple(request, work_slug, ref_slug):
	#ref = get_object_or_404(Ref, work__osis_slug=work_slug, osis_id=ref_slug)
	try: ref = Ref.objects.select_related('start_token', 'end_token').get(work__osis_slug=work_slug, osis_id=ref_slug)
	except: raise Http404
	tokens = ref.tokens
		
	return render_to_response('scripture_simple.html', { 'tokens': tokens })
	
def ajaxSlugs(request, work_slug, ref_start, ref_end=None):
	"""
	The complexity of this function is due to the fact that django doesn't yet support reverse lookups like ...
	Token.objects.select_related('token_parsing_set').filter( ... )
	Functionality like that would be a great asset especially in larger data sets like this.
	"""
	if not ref_end: ref_end = ref_start
	start_pos = ref_start.start_token.position - 1
	end_pos = ref_end.end_token.position + 1
	if ref_start != ref_end:
		tokens = Token.objects.filter(
			work__osis_slug = work_slug,
            position__gt = start_pos,
            position__lt = end_pos
        )
		title = str(ref_start) + ' &mdash; ' + str(ref_end)
	
	else:
		tokens = ref_start.tokens
		title = str(ref_start)
		
	token_dict = {}
	for tok in tokens:
		token_dict[tok.pk] = tok
		tok.start_refs = []
		tok.end_refs = []
		tok.parsing = ''
	
	### get refs for selected tokens
	### could do this in the template, but that results in 2 queries for every token (that's bad)
	start_refs = Ref.objects.filter(start_token__in=tokens)
	end_refs = Ref.objects.filter(end_token__in=tokens)
	
	for ref in start_refs: token_dict[ref.start_token_id].start_refs.append(ref)
	for ref in end_refs: token_dict[ref.end_token_id].end_refs.append(ref)
	
	for parse in TokenParsing.objects.filter(token__in=tokens):
		token_dict[parse.token_id].parsing = parse.raw
	
	return render_to_response(
		'scripture.html', {
			'tokens': tokens,
			'title': title,
		}
	)
		
	
### these two functions are used for ajax infinite-scroll functionality
def ajaxTokNext(request, work_slug, ref_slug):
	try: ref = Ref.objects.select_related('start_token', 'end_token').get(work__osis_slug=work_slug, osis_id=ref_slug)
	except: raise Http404
	return ajaxSlugs(request, work_slug, ref.next_ref)
	
def ajaxTokPrev(request, work_slug, ref_slug):
	try: ref = Ref.objects.select_related('start_token', 'end_token').get(work__osis_slug=work_slug, osis_id=ref_slug)
	except: raise Http404
	return ajaxSlugs(request, work_slug, ref.previous_ref)
	
def ajaxChapterNav(request, work_slug, ref_slug):
	book = Ref.objects.select_related('start_token', 'end_token').get(
		work__osis_slug = work_slug,
        osis_id = ref_slug
    )
	chapters = []
	for ref in book.get_chapters_verses():
		if ref.is_verse():
			chap = chapters[-1]
			if not hasattr(chap, 'verses'): chap.verses = []
			chap.verses.append(ref)
		elif ref.is_chapter():
			chapters.append(ref)
		
	return render_to_response(
		'nav_chapters.html', {
			'chapters': chapters,
		}
	)
	
def ajaxBookNav(request, work_slug):
	books = Ref.objects.filter(
		work__osis_slug = work_slug,
        type = Ref.BOOK
    )
		
	return render_to_response(
		'nav_books.html', {
			'books': books,
		}
	)