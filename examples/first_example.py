from htmlst.HTMLSentenceTokenizer import HTMLSentenceTokenizer

example_html_one = open('example_html_one.html', 'r').read()

parsed_sentences = HTMLSentenceTokenizer().feed(example_html_one)

print(parsed_sentences)
