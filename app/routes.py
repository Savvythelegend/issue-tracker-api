from flask import Blueprint, request, jsonify
from .models import Issue
from . import db
from .schemas import IssueCreate, IssueOut
from pydantic import ValidationError

bp = Blueprint('api', __name__)


@bp.route('/')
def index():
    return '✅ Issue Tracker API is running'


@bp.route('/issues', methods=['GET'])
def get_issues():
    """
    Get all issues
    ---
    responses:
      200:
        description: A list of all issues
    """
    issues = Issue.query.all()
    return jsonify([issue.to_dict() for issue in issues])


@bp.route('/issues', methods=['POST'])
def create_issue():
    """
    Create a new issue
    ---
    parameters:
      - name: body
        in: body
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
def get_issue(issue_id):
    issue = Issue.query.get_or_404(issue_id)
    return jsonify(issue.to_dict())


@bp.route('/issues/<int:issue_id>', methods=['PUT'])
def update_issue(issue_id):
    """
    Update an issue by ID
    ---
    parameters:
      - name: issue_id
        in: path
        type: integer
        required: true
        description: ID of the issue to update
      - name: body
        in: body
        required: true
        schema:
          properties:
            title:
              type: string
              description: New title (optional)
            description:
              type: string
              description: New description (optional)
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
def patch_issue(issue_id):
    """
    Partially update an issue by ID
    ---
    parameters:
      - name: issue_id
        in: path
        type: integer
        required: true
        description: ID of the issue to update
      - name: body
        in: body
        required: true
        schema:
          properties:
            status:
              type: string
              description: New status (optional)
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
def delete_issue(issue_id):
    """
    Delete an issue by ID
    ---
    parameters:
      - name: issue_id
        in: path
        type: integer
        required: true
        description: ID of the issue to delete
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
