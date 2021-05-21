from dict_words import words


def page_menu(language):
    """Меню"""
    menu = [
            {"name": words['home'][language], "url": "/"},
            {"name": words['encrypt'][language], "url": "/encrypt/"},
            {"name": words['decrypt'][language], "url": "/decrypt/"}
    ]
    return menu
