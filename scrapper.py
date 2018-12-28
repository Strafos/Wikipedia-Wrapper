import wikipedia
from pprint import pprint
import re
import sqlite3


def divide(sentences, tot_len):
    """Divide lines into two partitions"""
    idx = 0
    curr_len = 0
    while idx < len(sentences) - 1:
        if curr_len < tot_len/2 and curr_len + len(sentences[idx]) > tot_len/2:
            break
        curr_len += len(sentences[idx])
        idx += 1
    return ('.'.join(sentences[:idx]), '.'.join(sentences[idx:]))


def filter_lines(lines):
    # Filter for lines that can be typed on a qwerty keyboard
    pattern = r'^[a-zA-Z0-9.!@?#"$%&:\';()*\+,\/;\-=[\\\]\^_{|}<>~` ]+$'
    usable_lines = [line for line in lines if re.match(
        pattern, line) and len(line) > 150]
    print("after regex keyboard", len(usable_lines))

    # Filter for paragraphs that are too long. Split on period
    sizable_lines = []
    for line in usable_lines:
        paragraph_len = len(line)
        back = line
        while len(line) > 600:
            sentences = line.split(".")
            front, back = divide(sentences, paragraph_len)
            sizable_lines.append(front)
            line = back

        sizable_lines.append(back)
    print("after filtering long", len(sizable_lines))
    # print(len(sizable_lines[0]))
    # print(sizable_lines[0])

    return [line for line in sizable_lines if len(line) > 150]


def get_page(page_name):
    page = wikipedia.page(page_name)
    title = page.title
    content = page.content
    paragraphs = filter_lines(content.split('\n'))
    return (title, paragraphs)


def add_to_db(page_name):
    page_title, page_content = get_page(page_name)
    conn = sqlite3.connect('/home/zaibo/code/type/db/typetext.db')
    c = conn.cursor()

    c.execute("INSERT INTO pages VALUES(null, ?)", (page_title,))

    # print(len(page_content))
    # print((len(page_content[0])))
    titled_content = [(page_title, content) for content in page_content]
    c.executemany('INSERT INTO content VALUES (null, ?, ?)',
                  titled_content)

    conn.commit()
    conn.close()


# topics = ["Physics", "Time", "Philosophy", "Music", "Ancient Rome"]
# add_to_db("Time")
# add_to_db("Philosophy")
# add_to_db("Music")
# add_to_db("Ancient Rome")
add_to_db("Determinism")
add_to_db("Emergence")
add_to_db("Free_will")
