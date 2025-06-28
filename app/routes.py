from flask import Blueprint, request, jsonify
from .models import Issue
from . import db

bp = Blueprint('api', __name__)


@bp.route('/issues', methods=['GET'])
def get_issues():
    issues = Issue.query.all()
    return jsonify([issue.to_dict() for issue in issues])


@bp.route('/issues', methods=['POST'])
def create_issue():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    title = data.get('title')
    if not title:
        return jsonify({'error': 'Title is required'}), 400

    issue = Issue(title=title)
    db.session.add(issue)
    db.session.commit()

    return jsonify(issue.to_dict()), 201


@bp.route('/issues/<int:issue_id>', methods=['GET'])
def get_issue(issue_id):
    issue = Issue.query.get_or_404(issue_id)
    return jsonify(issue.to_dict())


@bp.route('/issues/<int:issue_id>', methods=['PUT'])
def update_issue(issue_id):
    issue = Issue.query.get_or_404(issue_id)
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    title = data.get('title')
    description = data.get('description')

    if title is not None:
        issue.title = title

    if description is not None:
        issue.description = description

    db.session.commit()

    return jsonify(issue.to_dict()), 200

@bp.route('/issues/<int:issue_id>', methods=['PATCH'])
def patch_issue(issue_id):
    issue = Issue.query.get_or_404(issue_id)
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    
    status = data.get('status')
    if status is not None:
        issue.status = status

    db.session.commit()

    return jsonify(issue.to_dict()), 200
    
   