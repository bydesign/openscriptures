from django.db import models
from django.db.models import Q
import logging


OSIS_BIBLE_BOOK_CODES = (
    #Gen Exod Lev Num Deut Josh Judg Ruth 1Sam 2Sam 1Kgs 2Kgs 1Chr 2Chr Ezra Neh Esth Job Ps Prov Eccl Song Isa Jer Lam Ezek Dan Hos Joel Amos Obad Jonah Mic Nah Hab Zeph Hag Zech Mal
    'Matt', 'Mark', 'Luke', 'John', 'Acts', 'Rom', '1Cor', '2Cor', 'Gal', 'Eph', 'Phil', 'Col', '1Thess', '2Thess', '1Tim', '2Tim', 'Titus', 'Phlm', 'Heb', 'Jas', '1Pet', '2Pet', '1John', '2John', '3John', 'Jude', 'Rev'
    #'Luke'
    #'Luke',
    #'Acts'
    #'1John',
    #'Phil',
    #'2John',
    #'3John',
    #'Jude'
)

OSIS_BOOK_NAMES = {
	"Gen": "Genesis",
	"Exod": "Exodus",
	"Lev": "Leviticus",
	"Num": "Numbers",
	"Deut": "Deuteronomy",
	"Josh": "Joshua",
	"Judg": "Judges",
	"Ruth": "Ruth",
	"1Sam": "1 Samuel",
	"2Sam": "2 Samuel",
	"1Kgs": "1 Kings",
	"2Kgs": "2 Kings",
	"1Chr": "1 Chronicles",
	"2Chr": "2 Chronicles",
	"Ezra": "Ezra",
	"Neh": "Nehemiah",
	"Esth": "Esther",
	"Job": "Job",
	"Ps": "Psalms",
	"Prov": "Proverbs",
	"Eccl": "Ecclesiastes",
	"Song": "Song of Solomon",
	"Isa": "Isaiah",
	"Jer": "Jeremiah",
	"Lam": "Lamentations",
	"Ezek": "Ezekiel",
	"Dan": "Daniel",
	"Hos": "Hosea",
	"Joel": "Joel",
	"Amos": "Amos",
	"Obad": "Obadiah",
	"Jonah": "Jonah",
	"Mic": "Micah",
	"Nah": "Nahum",
	"Hab": "Habakkuk",
	"Zeph": "Zephaniah",
	"Hag": "Haggai",
	"Zech": "Zechariah",
	"Mal": "Malachi",
	
	"Matt": "Matthew",
	"Mark": "Mark",
	"Luke": "Luke",
	"John": "John",
	"Acts": "Acts",
	"Rom": "Romans",
	"1Cor": "1 Corinthians",
	"2Cor": "2 Corinthians",
	"Gal": "Galatians",
	"Eph": "Ephesians",
	"Phil": "Philippians",
	"Col": "Colossians",
	"1Thess": "1 Thessalonians",
	"2Thess": "2 Thessalonians",
	"1Tim": "1 Timothy",
	"2Tim": "2 Timothy",
	"Titus": "Titus",
	"Phlm": "Philemon",
	"Heb": "Hebrews",
	"Jas": "James",
	"1Pet": "1 Peter",
	"2Pet": "2 Peter",
	"1John": "1 John",
	"2John": "2 John",
	"3John": "3 John",
	"Jude": "Jude",
	"Rev": "Revelation",
	
	"Bar": "Baruch",
	"AddDan": "Additions to Daniel",
	"PrAzar": "Prayer of Azariah",
	"Bel": "Bel and the Dragon",
	"SgThree": "Song of the Three Young Men",
	"Sus": "Susanna",
	"1Esd": "1 Esdras",
	"2Esd": "2 Esdras",
	"AddEsth": "Additions to Esther",
	"EpJer": "Epistle of Jeremiah",
	"Jdt": "Judith",
	"1Macc": "1 Maccabees",
	"2Macc": "2 Maccabees",
	"3Macc": "3 Maccabees",
	"4Macc": "4 Maccabees",
	"PrMan": "Prayer of Manasseh",
	"Sir": "Sirach/Ecclesiasticus",
	"Tob": "Tobit",
	"Wis": "Wisdom of Solomon"
}

# Todo: We need to figure out a better way to do ENUM

class Language(models.Model):
    "A human language, either ancient or modern."
    
    DIRECTIONS = (
        ('ltr', 'Left to Right'),
        ('rtl', 'Right to Left'),
        #also needing vertical directions, see CSS writing-mode
    )
    
    code = models.CharField("ISO language code", max_length=10, primary_key=True)
    name = models.CharField(max_length=32) #name = models.ForeignKey('Text', related_name='language_name_set') #Reverse query name for field 'name' clashes with field 'Text.language'. Add a related_name argument to the definition for 'name'.
    direction = models.CharField("Text directionality", max_length=3, choices=DIRECTIONS, default='ltr')
    
    def __unicode__(self):
        return self.name


#class Text(models.Model):
#    "A i18n construct. Used throughout the schema to store text."
#    
#    id = models.AutoField(primary_key=True) #this should eventually be primary_key together with language
#    language = models.ForeignKey('Language') 
#    data = models.TextField()
#    
#    def __unicode__(self):
#        return self.data


class License(models.Model):
    "A license that a work uses to indicate the copyright restrictions or permissions."
    
    name = models.CharField(max_length=128)  #name = models.ForeignKey(Text, related_name='license_name_set')
    abbreviation = models.CharField(max_length=32, null=True)  #abbreviation = models.ForeignKey(Text, null=True)
    url = models.URLField(null=True, help_text="Primary URL which defines and describes the license.")
    
    isolatable = models.BooleanField(default=True, help_text="If this is true, then this work can be displayed independently. Otherwise, it must only be displayed in conjunction with other works. Important condition for fair use license.")
    
    def __unicode__(self):
        return self.name


class Work(models.Model):
    """
    Represents an OSIS work. May be the Bible, a book of the Bible, an edition
    of the Bible, a non-biblical work such as the Qur'an or the Mishnah.
    """
    
    title = models.CharField(max_length=255)  #title = models.ForeignKey(Text, related_name='work_title_set')
    abbreviation = models.CharField(max_length=255, null=True) #abbreviation = models.ForeignKey(Text, null=True)
    description = models.TextField(null=True)
    url = models.URLField(null=True)
    
    ORIGINALITIES = (
        ('autograph', 'Autograph'),
        ('manuscript', 'Manuscript'),
        ('unified', 'Unified Work'),
        ('manuscript-edition', 'Manuscript Edition'),
        ('translation', 'Translation')
    )
    originality = models.CharField(max_length=32, choices=ORIGINALITIES, null=True, help_text="If NULL, then inherited from parent")
    
    TYPES = (
        ('Bible', "Bible"),
        ('Lexicon', 'Lexicon')
    )
    type = models.CharField(max_length=16, choices=TYPES, null=True, help_text="If NULL, then inherited from parent") #If NULL, then inherited from parent
    language = models.ForeignKey(Language, null=True, help_text="If NULL, then inherited from parent") #If NULL, then inherited from parent
    osis_slug = models.SlugField(max_length=255, help_text="OSIS identifier which should correspond to the abbreviation, like NIV, ESV, or KJV")
    #TODO: Needing edition and version?
    publish_date = models.DateField(null=True, help_text="When the work was published; if NULL, then inherited from parent")
    
    #returns Bible.en.NIV.1984, which is an osisID Prefix
    # Note: This is bad because it is not indexable
    def __getattr__(self, name):
        if name == 'osis_id':
            osis_id = []
            if self.type:
                osis_id.append(self.type)
            if self.language:
                osis_id.append(self.language)
            if self.osis_slug:
                osis_id.append(self.osis_slug)
            if self.publish_date:
                osis_id.append(self.publish_date.year)
            return ".".join(osis_id)
        else:
            raise AttributeError("The property %s does not exist" % name)
    
    base = models.ForeignKey('self', null=True, related_name="variants", help_text="If variant_number is not null, then 'base' is the work that contains this work's tokens where tokens.variant_number = self.variant_number")
    
    creator = models.TextField(null=True) #models.ForeignKey(Text, related_name='work_creator_set')
    copyright = models.TextField(null=True) #models.ForeignKey(Text, related_name='work_copyright_set')
    license = models.ForeignKey(License)
    
    unified = models.ForeignKey('self', null=True, verbose_name="Work which this work has been merged into")
    
    def __unicode__(self):
        return self.title
       
    class Meta:
        ordering = ['originality', 'type', 'language']

class VariantGroup(models.Model):
    work = models.ForeignKey(Work, help_text="The work which this variant group is associated with. If it is different from the token's work, then this variant group contains the tokens that are unique to that work.") #If set, it can either be the same as the base work, or a work that itself has a base  the title and description should be left empty; otherwise, then this variant group is not associated with any work, and the title and description can be provided if applicable.
    primacy = models.PositiveSmallIntegerField(null=False, default=0, help_text="A value of zero means that the tokens assigned to this token group are considered the most preeminent (i.e. they are displayed as the base text). Primacy values above zero indicate subordinate readings. The higher the number, the less precedence a token it has in relation to other token groups.")
    title = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    license = models.ForeignKey(License, null=True, help_text="If not specified, license is inherited from the work's license.")
    
    #class Meta:
    #    unique_together = (('work', 'primacy'),) #This may not be helpful

class VariantGroupToken(models.Model):
    "The many-to-many relationship between Token and VariantGroup goes through this model."
    token = models.ForeignKey('Token')
    variant_group = models.ForeignKey('VariantGroup')
    
    certainty = models.PositiveSmallIntegerField(default=0, null=False, help_text="Serves to indicate whether a token should be set apart with brackets, that is, if it is a less certain reading. The most certain readings are '0' (default). The number here corresponds to the number of square brackets that set apart this token. Overrides Token.certainty.")


class Token(models.Model):
    """
    The Token object represents a word, space, morpheme or punctuation in the text.
    Changes are now tracked using the TokenHistory model.
    """
    
    MORPHEME = 1
    WORD = 2
    PUNCTUATION = 3
    WHITESPACE = 4
    _parsing = ''
    
    TYPES = (
        (MORPHEME,    'Morpheme'),
        (WORD,        'Word'),
        #(PHRASE,        'Phrase'),
        (PUNCTUATION, 'Punctuation'),
        (WHITESPACE,  'Whitespace'),
    )
    
    data = models.CharField(max_length=255, db_index=True)
    type = models.PositiveSmallIntegerField(choices=TYPES, default=WORD, db_index=True, help_text="Morphemes do not automatically get whitespace padding, words do (TENTATIVE).")
    position = models.PositiveIntegerField(db_index=True)
    position2 = models.PositiveIntegerField(db_index=True)  ### this field is so tokens can be added without reindexing the entire work
    certainty = models.PositiveSmallIntegerField(default=0, null=True, help_text="Serves to indicate whether a token should be set apart with brackets, that is, if it is a less certain reading. The most certain readings are '0' (default). The number here corresponds to the number of square brackets that set apart this token. Overridden by VariantGroupToken.certainty (in that case, self.certainty may be None)")
    unified_token = models.ForeignKey('self', null=True, help_text="The token in the merged/unified work that represents this token. unified_token.originality should be 'unified'")
    work = models.ForeignKey(Work, db_index=True)
    #variant_group = models.ForeignKey(VariantGroup, null=True, help_text="The grouping of variants that this token belongs to; if empty, token is common to all variant groups associated with this token's work, including all tokens of all works that point to this token's work as their base.")
    variant_groups = models.ManyToManyField(VariantGroup, through=VariantGroupToken, null=True, help_text="The groupings of variants (associated with this work or its sub-works) that this token belongs to; if none provided, then token is common to all variant groups associated with this token's work, including all tokens of all works that point to this token's work as their base.")
    
    cmp_data = None
    def __unicode__(self):
        if(self.cmp_data):
            return self.cmp_data
        return ('[' * self.certainty) + self.data + (']' * self.certainty)
    
    def __hash__(self):
        return hash(unicode(self))
    
    def __eq__(self, other):
        return unicode(self) == unicode(other)
    
    def get_parsing(self):
    	if self._parsing: return self._parsing
    	parse = ''
    	for parsing in self.token_parsing_set.all():
    		parse += parsing.raw
    		parse += '1 '
    	return parse
    def set_parsing(self, str):
    	self._parsing = str
    parsing = property(get_parsing, set_parsing)
       
    def get_ref(self, ref_type=1):
    	return Ref.objects.get(
    		work = self.work,
    		type = ref_type,
    		start_token__position__lte = self.position,
    		end_token__position__gte = self.position
    	)
    	
    def get_verse(self): return self.get_ref(Ref.VERSE)
    verse = property(get_verse)
    def get_chapter(self): return self.get_ref(Ref.CHAPTER)
    chapter = property(get_chapter)
    def get_book(self): return self.get_ref(Ref.BOOK)
    book = property(get_book)
    
    class Meta:
        ordering = ['position',]
        #Note: This unique constraint is removed due to the fact that in MySQL, the default utf8 collation means "Και" and "καὶ" are equivalent
        #unique_together = (
        #    ('data', 'position', 'work'),
        #)

#class NormalizedToken(Token):
#    class Meta:
#        proxy = True


class TokenParsing(models.Model):
    "This is a temporary construct until language-specific parsing models are constructed."
    token = models.ForeignKey(Token, related_name='token_parsing_set')
    raw = models.CharField(max_length=255, help_text="All parsing information provided verbatim")
    parse = models.CharField(max_length=255, help_text="A string consisting of whatever the work provides; the unparsed parsing. Likely consisting of the lemma, Strong's number, morph, etc. This is temporary until we can integrate with lemma lattice.  Temporary measure until Lemma Lattice released")
    strongs = models.CharField(max_length=255, help_text="The strongs number, prefixed by 'H' or 'G' specifying whether it is for the Hebrew or Greek, respectively. Multiple numbers separated by semicolon. Temporary measure until Lemma Lattice released.")
    lemma = models.CharField(max_length=255, help_text="The lemma chosen for this token. Need not be supplied if strongs given. If multiple lemmas are provided, then separate with semicolon.  Temporary measure until Lemma Lattice released")
    language = models.ForeignKey(Language)
    work = models.ForeignKey(Work, null=True, help_text="The work that defines this parsing; may be null since a user may provide it. Usually same as token.work")
    
    def __unicode__(self):
    	return self.raw
    
    
class SemanticLink(models.Model):
    """
    A SemanticLink is created to link tokens in a translation with tokens in the unified text.
    This will be primarily used by the semantic linker app for creating the data (crowdsourcing?)
    The data will 
    """
    original_tokens = models.ManyToManyField(Token)
    translated_tokens = models.ManyToManyField(Token)
 
 
class Selection(models.Model):
    """
    This is the base model for any descriptor of a group of tokens.
    It 'contains' all tokens between start_token and end_token within the work.
    Multitable inheritance is used for classes like Ref to extend this model.
    The study app also has many models that inherit from this one.
    """
    start_token = models.ForeignKey(Token, related_name='start_selection_set')
    end_token = models.ForeignKey(Token, related_name='end_selection_set')
    work = models.ForeignKey(Work)
    

class Ref(Selection):
    BOOK_GROUP = 1
    BOOK = 2
    MAJOR_SECTION = 3
    SECTION = 4
    PARAGRAPH = 5
    CHAPTER = 6
    VERSE = 7
    PAGE = 8
    
    TYPES = (
        (BOOK_GROUP,    'bookGroup'),
        (BOOK,          'book'),
        (MAJOR_SECTION, 'majorSection'),
        (SECTION,       'section'),
        (PARAGRAPH,     'paragraph'),
        (CHAPTER,       'chapter'),
        (VERSE,         'verse'),
        (PAGE,          'page')
    )
    
    work = models.ForeignKey(Work, null=True, help_text="If this ref is for a work that relies on a base work, this value does not point to the base work; that is, if two works are merged together, with one being the base work, then each work has its own references stored, and they refer to their respective works, not the base work.")
    type = models.PositiveSmallIntegerField(choices=TYPES)
    osis_id = models.CharField(max_length=50, db_index=True)
    position = models.PositiveIntegerField(db_index=True)
    title = models.CharField(max_length=50)
    parent = models.ForeignKey('self', null=True)
    #start_token = models.ForeignKey(Token, related_name='start_token_ref_set') #, help_text="This can be null for convienence while creating objects, but it should not end up being null."
    #end_token = models.ForeignKey(Token, null=True, related_name='end_token_ref_set')
    #numerical_start = models.PositiveIntegerField(null=True)
    #numerical_end = models.PositiveIntegerField(null=True)

    def get_tokens(self, variant_number = 1):
		"""
		This function returns the tokens contained by a particular reference.
		When calling this function, it will spawn 2 new queries unless you've already done:
		Ref.objects.select_related('start_token', 'end_token').get( ... )
		Querying your Ref object this way will prevent the unecessary extra queries.
		"""
		return Token.objects.select_related('start_token_ref_set', 'end_token_ref_set', 'token_parsing_set').filter(
		    #Q(variant_number = None) | Q(variant_number = variant_number),
		    work__id = self.work_id,
		    position__gte = self.start_token.position,
		    position__lte = self.end_token.position
		    #position__in = range(self.start_token.position, self.end_token.position)
		)
    tokens = property(get_tokens)
    
    def __unicode__(self):
    	osis_parts = self.osis_id.split('.')
    	ref = OSIS_BOOK_NAMES[osis_parts[0]]
    	if len(osis_parts) > 1: ref += ' ' + osis_parts[1]
    	if len(osis_parts) > 2: ref += ':' + osis_parts[2]
    	
    	return ref
    	
    def __hash__(self):
        return hash(unicode(self))
    
    def __eq__(self, other):
        return unicode(self) == unicode(other)
    
    def __unicode__(self):
        if self.type == Ref.PAGE:
            if not self.numerical_end or self.numerical_end == self.numerical_start:
                return "p. " + self.numerical_start
            else:
                return "pp. " + self.numerical_start + "-" + self.numerical_end
        return self.osis_id
    
    def is_book_group(self):    return self.type == self.BOOK_GROUP
    def is_book(self):          return self.type == self.BOOK
    def is_major_section(self): return self.type == self.MAJOR_SECTION
    def is_section(self):       return self.type == self.SECTION
    def is_paragraph(self):     return self.type == self.PARAGRAPH
    def is_chapter(self):       return self.type == self.CHAPTER
    def is_verse(self):         return self.type == self.VERSE
    
    def get_verse_numbers(self):
		if self.is_verse():
			osis_parts = self.osis_id.split('.')
			ch = osis_parts[1]
			v =  osis_parts[2]
			return ch + ':' + v
		else:
			return ''
    verse_numbers = property(get_verse_numbers)
	
	### these two functions are used for ajax infinite-scroll functionality
    def get_previous_ref(self):
    	return Ref.objects.select_related('start_token', 'end_token').get(end_token__position=self.start_token.position-1, work__id=self.work_id, type=self.type)
    previous_ref = property(get_previous_ref)
	
    def get_next_ref(self):
    	return Ref.objects.select_related('start_token', 'end_token').get(start_token__position=self.end_token.position+1, work__id=self.work_id, type=self.type)
    next_ref = property(get_next_ref)
    
    def get_inner_refs(self, ref_type=None):
    	refs = Ref.objects.select_related('start_token','end_token').filter(
			start_token__position__gte = self.start_token.position,
			end_token__position__lte = self.end_token.position,
			work__id = self.work_id)
    	
    	if ref_type: refs = refs.filter(type = ref_type)
    	
    	return refs
    
    def get_chapters_verses(self):
		refs = Ref.objects.filter(
			Q(type = self.VERSE) | Q(type = self.CHAPTER),
			start_token__position__gte = self.start_token.position,
			end_token__position__lte = self.end_token.position,
			work__id = self.work_id
		)
		return refs
    		
    """def get_inner_verses(self):
    	return self.get_inner_refs(self.VERSE)
    inner_verses = property(get_inner_verses)
    		
    def get_inner_chapters(self):
    	return self.get_inner_refs(self.CHAPTER)
    inner_chapters = property(get_inner_chapters)"""

    
class Note(Selection):
    title = models.CharField(max_length=255)
    body = models.TextField()
    current = models.BooleanField(default=True, blank=True)

class Thread(Selection):
    title = models.CharField(max_length=255)
    
class Post(models.Model):
    created = models.DateTimeField(auto_add_now=True, editable=False)
    thread = models.ForeignKey(Thread)
    parent = models.ForeignKey('self', blank=True, null=True)
    title = models.CharField(max_length=255)
    body = models.TextField()
    

### the following classes are used for versioning and revisions
### this is primarily used for translation purposes (starting with NET Bible)
class Revision(models.Model):
    created = models.DateTimeField(auto_add_now=True, editable=False)
    number = models.IntegerField()
    work = models.ForeignKey(Work)
    
class TokenHistory(models.Model):
    MORPHEME = Token.MORPHEME
    WORD = Token.WORD
    PUNCTUATION = Token.PUNCTUATION
    TYPES = Token.TYPES
    
    created = models.DateTimeField(auto_add_now=True, editable=False)
    data = models.CharField(max_length=255)
    type = models.PositiveSmallIntegerField(choices=TYPES, default=WORD, help_text="Morphemes do not automatically get whitespace padding, words do (TENTATIVE).")
    position = models.PositiveIntegerField(db_index=True)
    position2 = models.PositiveIntegerField(db_index=True)
    certainty = models.PositiveSmallIntegerField(default=0, null=False, help_text="Serves to indicate whether a token should be set apart with brackets, that is, if it is a less certain reading. The most certain readings are '0' (default). The number here corresponds to the number of square brackets that set apart this token.")
    unified_token = models.ForeignKey('self', null=True, help_text="The token in the merged/unified work that represents this token. unified_token.originality should be 'unified'")
    work = models.ForeignKey(Work, db_index=True)
    variant_number = models.PositiveSmallIntegerField(null=True, default=None, db_index=True, help_text="If null, then this token is attested to by the base work and all associated variant works. If not null, then this number may correspond to a work.variant_number; alternatively, it may not correspond and in this case it is an anonymous variant.")
    
    def __unicode__(self):
        if(self.cmp_data):
            return self.cmp_data
        return ('[' * self.certainty) + self.data + (']' * self.certainty)
    
class NoteHistory(Selection):
    created = models.DateTimeField(auto_add_now=True, editable=False)
    title = models.CharField(max_length=255)
    body = models.TextField()
    current = models.BooleanField(default=True, blank=True)

