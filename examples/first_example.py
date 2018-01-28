from HTMLSentenceTokenizer import HTMLSentenceTokenizer

example_html_one = open('example_html_one.html', 'r').read()

tokenizer = HTMLSentenceTokenizer()
parsed_sentences = tokenizer.feed(example_html_one)

print(parsed_sentences)
