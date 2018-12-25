import wikipedia
from pprint import pprint
import re
import sqlite3


def filter_lines(lines):
    """Filter for lines that can be typed on a qwerty keyboard"""
    pattern = r'^[a-zA-Z0-9.!@?#"$%&:\';()*\+,\/;\-=[\\\]\^_{|}<>~` ]+$'
    return [line for line in lines if not re.match(pattern, line) and len(line) > 100]


def get_page(page_name):
    page = wikipedia.page(page_name)
    title = page.title
    content = page.content
    paragraphs = filter_lines(content.split('\n'))
    return (title, paragraphs)


page_title, page_content = get_page("Physics")
conn = sqlite3.connect('/home/zaibo/code/type/db/typetext.db')
c = conn.cursor()

c.execute("INSERT INTO pages VALUES(null, ?)", (page_title,))

titled_content = [(page_title, content) for content in page_content]
c.executemany('INSERT INTO content VALUES (null, ?, ?)', titled_content)

conn.commit()
conn.close()

# print(filter_lines(["hello", "damn.", "%", "foo!"]))
