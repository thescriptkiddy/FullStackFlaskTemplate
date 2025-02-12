def get_mock_menu_data():
    mock_menu_data = [
        {
            'id': 1,
            'name': 'Main Menu',
            'links': [
                {'id': 1, 'name': 'Home', 'url': 'home.index', 'title': 'Home'},
                {'id': 2, 'name': 'Menus', 'url': 'menu.index', 'title': 'Menus'},
                {'id': 3, 'name': 'Users', 'url': 'users.users_index', 'title': 'Users'},
                {'id': 4, 'name': 'Items', 'url': 'items.items_index', 'title': 'Items'}
            ]
        },
        {
            'id': 2,
            'name': 'Footer Menu',
            'links': [
                {'id': 3, 'name': 'Users', 'url': 'users.users_index', 'title': 'Users'},
                {'id': 4, 'name': 'Items', 'url': 'items.items_index', 'title': 'Items'}
            ]
        }
    ]
    return mock_menu_data
