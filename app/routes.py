from flask import Blueprint, request, jsonify
from .models import Issue, User, BlackListTokens
from .schemas import IssueCreate, IssueOut
from pydantic import ValidationError
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity, create_refresh_token, get_jwt
)

bp = Blueprint('api', __name__)

@bp.route('/')
def index():
    return """
    <html>
        <head>
            <style>
                .loader {
                  border: 8px solid #f3f3f3;
                  border-top: 8px solid #3498db;
                  border-radius: 50%;
                  width: 60px;
                  height: 60px;
                  animation: spin 2s linear infinite;
                }

                @keyframes spin {
                  0% { transform: rotate(0deg); }
                  100% { transform: rotate(360deg); }
                }
            </style>
        </head>
        <body>
            <h2>Issue Tracker API</h2>
            <div class="loader"></div>
        </body>
    </html>
    """

@bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
          properties:
            email:
              type: string
            password:
              type: string
    responses:
      201:
        description: User registered
      400:
        description: Invalid input or user exists
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON in request"}), 400

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "User already exists"}), 400

    new_user = User(email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


@bp.route('/login', methods=['POST'])
def login():
    """
    Login and receive a JWT token
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
          properties:
            email:
              type: string
            password:
              type: string
    responses:
      200:
        description: Returns a JWT access token
      400:
        description: Missing or invalid input
      401:
        description: Invalid credentials
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON in request"}), 400

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    return jsonify(access_token=access_token, refresh_token=refresh_token), 200



@bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """
    Refresh access token
    ---
    security:
      - Bearer: []
    responses:
      200:
        description: New access token issued
      401:
        description: Invalid or expired refresh token
    """
    user_id = get_jwt_identity()
    access_token = create_access_token(identity=user_id)
    return jsonify(access_token=access_token), 200


@bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """
    Logout user and blacklist the token
    ---
    security:
      - Bearer: []
    responses:
      200:
        description: Token successfully revoked
      401:
        description: Invalid or missing token
    """
    jti = get_jwt()["jti"]
    db.session.add(BlackListTokens(jti=jti))
    db.session.commit()
    return jsonify({"message": "Logged out successfully"}), 200

@bp.route('/logout-refresh', methods=['POST'])
@jwt_required
def logout_ref():
    jti = get_jwt["jti"]
    db.session.add(BlackListTokens(jti=jti))
    db.session.commit()
    return jsonify('{msg: "Refesh token revoked"}'), 200

@bp.route('/issues', methods=['POST'])
@jwt_required()
def create_issue():
    """
    Create a new issue
    ---
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          properties:
            title:
              type: string
            description:
              type: string
    responses:
      201:
        description: Issue created
    """
    try:
        issue_data = IssueCreate(**request.get_json())
    except ValidationError as e:
        return jsonify({'error': e.errors()}), 400

    issue = Issue(title=issue_data.title, description=issue_data.description)
    db.session.add(issue)
    db.session.commit()

    return jsonify(IssueOut(id=issue.id, title=issue.title, description=issue.description).dict()), 201


@bp.route('/issues/<int:issue_id>', methods=['GET'])
@jwt_required()
def get_issue(issue_id):
    """
    Get a single issue by ID
    ---
    security:
      - Bearer: []
    parameters:
      - name: issue_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Returns issue
      404:
        description: Issue not found
    """
    issue = Issue.query.get_or_404(issue_id)
    return jsonify(issue.to_dict())


@bp.route('/issues/<int:issue_id>', methods=['PUT'])
@jwt_required()
def update_issue(issue_id):
    """
    Fully update an issue by ID
    ---
    security:
      - Bearer: []
    parameters:
      - name: issue_id
        in: path
        type: integer
        required: true
      - in: body
        name: body
        required: true
        schema:
          properties:
            title:
              type: string
            description:
              type: string
    responses:
      200:
        description: The updated issue
      404:
        description: Issue not found
    """
    issue = Issue.query.get_or_404(issue_id)

    try:
        update_data = IssueCreate(**request.get_json())
    except ValidationError as e:
        return jsonify({'error': e.errors()}), 400

    issue.title = update_data.title
    issue.description = update_data.description
    db.session.commit()

    return jsonify(IssueOut(id=issue.id, title=issue.title, description=issue.description).dict()), 200


@bp.route('/issues/<int:issue_id>', methods=['PATCH'])
@jwt_required()
def patch_issue(issue_id):
    """
    Partially update an issue by ID
    ---
    security:
      - Bearer: []
    parameters:
      - name: issue_id
        in: path
        type: integer
        required: true
      - in: body
        name: body
        required: true
        schema:
          properties:
            status:
              type: string
              description: New status
    responses:
      200:
        description: The updated issue
      404:
        description: Issue not found
    """
    issue = Issue.query.get_or_404(issue_id)
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    status = data.get('status')
    if status is not None:
        issue.status = status

    db.session.commit()
    return jsonify(issue.to_dict()), 200


@bp.route('/issues/<int:issue_id>', methods=['DELETE'])
@jwt_required()
def delete_issue(issue_id):
    """
    Delete an issue by ID
    ---
    security:
      - Bearer: []
    parameters:
      - name: issue_id
        in: path
        type: integer
        required: true
    responses:
      204:
        description: Issue deleted
      404:
        description: Issue not found
    """
    issue = Issue.query.get_or_404(issue_id)
    db.session.delete(issue)
    db.session.commit()
    return '', 204
