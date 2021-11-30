def html_bold(text):
    return u"<b>{}</b>".format(text)


def html_italic(text):
    return u"<i>{}</i>".format(text)


def html_bold_italic(text):
    return u"<b><i>{}</i></b>".format(text)


def html_underline(text):
    return u"<u>{}</u>".format(text)


def html_url(text, url):
    return u'<a href="{}">{}</a>'.format(url, text)


def html_blockquote(klass, text):
    return u'<blockquote class="{}">{}</blockquote>'.format(klass, text)


def html_heading(text, level=1):
    return u'<h{level}>{text}</h{level}>'.format(text=text, level=level)


def md_unformatted(text):
    return u'```\n{}\n```'.format(text)


def md_list(items):
    return u''.join([u"- {}\n".format(item) for item in items])
