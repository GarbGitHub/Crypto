def page_menu():
    """Меню для авторизованных пользователей"""
    menu = [
            {"name": "Home", "url": "/"},
            {"name": "Encrypt", "url": "/encrypt/"},
            {"name": "Decrypt", "url": "/decrypt/"}
    ]

    return menu
