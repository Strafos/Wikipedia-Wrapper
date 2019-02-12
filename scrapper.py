import wikipedia
from pprint import pprint
import re
import sqlite3

LENGTH_THRESHOLD = 300


def divide(sentences, threshold):
    """Divide lines into two partitions"""
    idx = 0
    curr_len = 0
    while idx < len(sentences) - 1:
        if curr_len < threshold and curr_len + len(sentences[idx]) > threshold:
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
        back = line
        while len(line) > LENGTH_THRESHOLD:
            sentences = line.split(".")
            front, back = divide(sentences, LENGTH_THRESHOLD)
            sizable_lines.append(front)
            if line == back:
                break
            line = back

        sizable_lines.append(back)
    print("after filtering long", len(sizable_lines))

    processed_lines = []
    for line in sizable_lines:
        if len(line) < LENGTH_THRESHOLD and len(line) > 150:
            if line[0] == " ":
                line = line[1:]
            if line[-1] != '.':
                line += "."
            processed_lines.append(line)

    return processed_lines


def get_page(page_name):
    page = wikipedia.page(page_name)
    title = page.title
    content = page.content
    paragraphs = filter_lines(content.split('\n'))
    return (title, paragraphs)


def add_to_db(page_name):
    conn = sqlite3.connect('/home/zaibo/code/type/db/typetext.db')
    c = conn.cursor()
    page_title, page_content = get_page(page_name)

    c.execute("INSERT INTO pages VALUES(null, ?)", (page_title,))

    # print(len(page_content))
    # print((len(page_content[0])))
    titled_content = [(page_title, content, 0) for content in page_content]
    c.executemany('INSERT INTO content VALUES (null, ?, ?, ?)',
                  titled_content)

    conn.commit()
    conn.close()


# topics = ["Physics", "Time", "Philosophy", "Music", "Ancient Rome"]
# add_to_db("Time")
# add_to_db("Philosophy")
# add_to_db("Music")
# add_to_db("Ancient Rome")
# add_to_db("Determinism")
# add_to_db("Emergence")
# add_to_db("Free_will")
# add_to_db("Sociology")
# add_to_db("Psychology")
# add_to_db("Computer Science")
# add_to_db("Information theory")
# add_to_db("Math")
add_to_db("Time")
# add_to_db("Rome")
# add_to_db("Perception")
# add_to_db("Default Mode Network")
# add_to_db("Neuroscience")
