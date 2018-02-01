from examples.speed.calculate_time import calculate_time
from htmlst.HTMLSentenceTokenizer import HTMLSentenceTokenizer


markup = """
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
"""


def f():
    h = HTMLSentenceTokenizer()
    h.feed(markup)


range_loops = 1
for i in range(range_loops):
    with open('speed.txt', 'a') as file:
        file.write(str(calculate_time(f)) + "\n")
