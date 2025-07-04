from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt_identity

from ..models import User


def owner_or_admin_required(model, id_kwarg="issue_id", owner_field="user_id"):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            resource_id = kwargs.get(id_kwarg)
            resource = model.query.get_or_404(resource_id)

            current_user = User.query.get(get_jwt_identity())

            if (
                getattr(resource, owner_field) != current_user.id
                and current_user.role != "admin"
            ):
                return jsonify({"error": "Unauthorized"}), 403

            return f(*args, **kwargs)

        return wrapper

    return decorator
