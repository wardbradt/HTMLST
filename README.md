# HTMLSentenceTokenizer (HTMLST)
A library which extracts sentences from HTML

HTMLST breaks down HTML documents into paragraph-like sections by taking into account the [HTML5 Specification](https://html.spec.whatwg.org/multipage/) and web developers' typical usage of HTML tags and tokenizes the sentences in these sections using [NLTK](https://github.com/nltk/nltk)'s [Punkt Sentence Tokenizer](http://www.nltk.org/_modules/nltk/tokenize/punkt.html) to disambiguate sentence boundaries.

## Example:
`HTMLSentenceTokenizer` can parse the following HTML in one line.
```
<!DOCTYPE html>
<html lang="en">
<head>
</head>
<body>
<div>
    <h1>Header One</h1>
    Hello, my <span id="foo">name</span> is Geronimo. What's yours?
    <div>
        Here is a cool picture:
        <br>
        <img src="http://www.sourcecertain.com/img/Example.png">

        Now, isn't that nice?
    </div>

    He<span>r<b>e</b></span>'s a wei<mark>rd</mark> sen<b>t<i>e<span>n</span>c</i>e wit</b>h <i>lots</i> of inline tags.
</div>
</body>
</html>
```
The following code prints out the sentences of this HTML, which is stored in `example_html_one.html`.
```
from htmlst import HTMLSentenceTokenizer

example_html_one = open('example_html_one.html', 'r').read()
parsed_sentences = HTMLSentenceTokenizer().feed(example_html_one)
print(parsed_sentences)
```
The output is `['Hello, my name is Geronimo.', "What's yours?", 'Here is a cool picture:', "Now, isn't that nice?", "Here's a weird sentence with lots of inline tags."]`.

## Installation:
HTMLST is available on [pip](https://pypi.python.org/pypi/htmlst/0.1.0b1).
To install, enter the following into terminal:
```
pip install htmlst
```
