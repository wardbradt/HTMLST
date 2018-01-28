import html5lib
from nltk.tokenize import sent_tokenize

INLINE_ELEMENTS = ['a', 'abbr', 'acronym', 'b', 'bdi', 'bdo', 'big', 'cite', 'code', 'dfn', 'em', 'i', 'kbd',
                   'label', 'mark', 'nav', 'output', 'progress', 'q', 's', 'slot', 'small', 'span', 'strong',
                   'sub', 'sup', 'time', 'tt', 'var']

# does not include pre or textarea (which are accounted for in PRESERVE_WHITESPACE_ELEMENTS
BLOCK_LEVEL_ELEMENTS = ['address', 'article', 'blockquote', 'button', 'caption', 'details', 'dialog', 'div', 'dl',
                        'dt', 'figcaption', 'footer', 'form', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'header', 'hgroup',
                        'hr', 'li', 'main', 'ol', 'p', 'ul', 'section', 'table', 'tbody', 'td', 'th', 'thead', 'tr']

SKIPPED_ELEMENTS = ["br", "hr"]

EMPTY_ELEMENTS = ["area", "base", "embed", "img"]

PRESERVE_WHITESPACE_ELEMENTS = {'pre', 'textarea', 'button'}


class HTMLSentenceTokenizer:

    def __init__(self):
        # self.parser is an etree parser by default.
        self.parser = html5lib.HTMLParser()
        self.walker = html5lib.getTreeWalker("etree")
        self.sentences = []
        self.reset()

    def feed(self, markup):
        """
        Given an HTML document which contains tags on only INLINE_ELEMENTS, BLOCK_LEVEL_ELEMENTS, or
        PRESERVE_WHITESPACE_ELEMENTS, parses the HTML document into a BeautifulSoup-like tree represented by Node
        and TextNode objects. Stores these objects in the database. At the end, also resets this SentenceParser object
        by calling the reset() method.

        :return: The root node of the parsed tree.
        """
        etree_document = self.parser.parse(markup)
        stream = self.walker(etree_document)

        # todo: find a more efficient way to only iterate over tags that are a descendant of body
        passed_body = False

        for i in stream:
            if passed_body:
                if i['type'] == 'StartTag':
                    self.handle_starttag(i['name'], i['data'])
                elif i['type'] == 'EndTag':
                    if i['name'] == 'body':
                        break
                    self.handle_endtag(i['name'])
                # todo: handle space at end of text. for example, "<span>I like to eat </span><span>apples</span>" vs
                # "<span>I like to eat</span><span>apples</span>"
                elif i['type'] == 'Characters' or (i['type'] == 'SpaceCharacters' and self.ignored_element_count > 0):
                    self.handle_text(i['data'])
                elif i['type'] == 'SpaceCharacters':
                    self.handle_text(' ')
                elif i['type'] == 'SerializeError':
                    print(i['data'])
                # is comment, doctype, entity, or unknown.
                else:
                    pass
            elif i['type'] == 'StartTag' and i['name'] == 'body':
                passed_body = True

        sentences_copy = self.sentences
        self.reset()
        return sentences_copy

    def reset(self):
        self.sentences = []
        self.ignored_element_count = 0
        self.current_string = ''
        # how many inline tags are in the current section of the most recently processed block level element's children
        self.inlines_before_block = 0

    def handle_text(self, text):
        if self.ignored_element_count > 0:
            return

        self.current_string += text

    def handle_starttag(self, tag_name, attrs):
        # if tag is the child of a pre or textarea tag
        if self.ignored_element_count > 0:
            if tag_name in PRESERVE_WHITESPACE_ELEMENTS:
                self.ignored_element_count += 1

            self.inlines_before_block += 1
            return

        if tag_name in INLINE_ELEMENTS:
            return

        if tag_name in PRESERVE_WHITESPACE_ELEMENTS:
            self.handle_end_of_string()

            self.ignored_element_count += 1
            return

        if tag_name in BLOCK_LEVEL_ELEMENTS:
            self.handle_end_of_string()
            return

        raise ValueError("parsing a tag which is not in the accepted element types. It is of type {}".format(tag_name))

    def handle_endtag(self, tag):
        if tag in PRESERVE_WHITESPACE_ELEMENTS:
            self.ignored_element_count -= 1
            return

        # if in a PWE (and tag is not a PWE), add ClosingSimpleTag to current_iteration_queue.
        if self.ignored_element_count > 0:
            return

        if tag in INLINE_ELEMENTS:
            return

        if tag in BLOCK_LEVEL_ELEMENTS:
            self.handle_end_of_string()
            return

    # todo:
    def handle_startendtag(self, tag, attrs):
        pass

    def handle_end_of_string(self):
        self.sentences += sent_tokenize(self.current_string)
        self.current_string = ''
