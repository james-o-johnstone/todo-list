from flask_login import current_user


def jsonify_item(item):
    return {
        'item': {
            'completed': item.completed,
            'description': item.description,
            'id': str(item.id),
            'title': item.title,
            'user_id': str(current_user.id),
        }
    }