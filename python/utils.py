
LINK = "<link>"
LINK_LENGTH = len(LINK)
END_LINK = "</link>"
END_LINK_LENGTH = len(END_LINK)
NOT_FOUND = -1

def find_links(links, response):
    l = response.find(LINK)
    if l == NOT_FOUND:
        return
    else:
        e = response.find(END_LINK)
        links.append(response[l+LINK_LENGTH:e])
        return find_links(links, response[e+END_LINK_LENGTH:])
