import wikipedia


def get_wiki_page(page_name):
    print(wikipedia.summary("Wikipedia"))


get_wiki_page("foo")
