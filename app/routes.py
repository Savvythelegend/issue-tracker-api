import logging

from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)
from pydantic import ValidationError

from .decorators.rbac import owner_or_admin_required
from .extensions import db
from .models import BlackListTokens, Issue, User
from .schemas import IssueCreate, IssueOut, UserIn

bp = Blueprint("api", __name__)
logger = logging.getLogger(__name__)


@bp.route("/")
def index():
    return """<html><head><style>.loader {
      border: 8px solid #f3f3f3;
      border-top: 8px solid #3498db;
      border-radius: 50%;
      width: 60px;
      height: 60px;
      animation: spin 2s linear infinite;
    } @keyframes spin {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }</style></head><body><h2>Issue Tracker API</h2><div class=\"loader\"></div></body></html>"""


@bp.route("/register", methods=["POST"])
def register():
    try:
        user_data = UserIn(**request.get_json())
    except ValidationError as e:
        logger.warning("Invalid registration input: %s", e.errors())
        return jsonify({"error": e.errors()}), 400

    if User.query.filter_by(email=user_data.email).first():
        logger.warning("Attempt to register with existing email: %s", user_data.email)
        return jsonify({"error": "User already exists"}), 400

    new_user = User(email=user_data.email, role="user")
    new_user.set_password(user_data.password)
    db.session.add(new_user)
    db.session.commit()

    logger.info("User registered: %s", user_data.email)
    return jsonify({"message": "User registered successfully"}), 201


@bp.route("/login", methods=["POST"])
def login():
    try:
        user_data = UserIn(**request.get_json())
    except ValidationError as e:
        logger.warning("Invalid login input")
        return jsonify({"error": e.errors()}), 400

    user = User.query.filter_by(email=user_data.email).first()
    if not user or not user.check_password(user_data.password):
        logger.warning("Invalid login credentials for email: %s", user_data.email)
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(
        identity=user.id, additional_claims={"role": user.role}
    )
    refresh_token = create_refresh_token(identity=user.id)

    logger.info("User logged in: %s", user.email)
    return jsonify(access_token=access_token, refresh_token=refresh_token), 200


@bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    access_token = create_access_token(identity=user_id)
    logger.info("Access token refreshed for user %s", user_id)
    return jsonify(access_token=access_token), 200


@bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    db.session.add(BlackListTokens(jti=jti))
    db.session.commit()
    logger.info("Access token blacklisted (logout): %s", jti)
    return jsonify({"message": "Logged out successfully"}), 200


@bp.route("/logout-refresh", methods=["POST"])
@jwt_required(refresh=True)
def logout_refresh():
    jti = get_jwt()["jti"]
    db.session.add(BlackListTokens(jti=jti))
    db.session.commit()
    logger.info("Refresh token blacklisted (logout): %s", jti)
    return jsonify({"message": "Refresh token revoked"}), 200


@bp.route("/issues", methods=["POST"])
@jwt_required()
def create_issue():
    try:
        issue_data = IssueCreate(**request.get_json())
    except ValidationError as e:
        logger.warning("Invalid issue creation data: %s", e.errors())
        return jsonify({"error": e.errors()}), 400

    user_id = get_jwt_identity()
    issue = Issue(
        title=issue_data.title, description=issue_data.description, user_id=user_id
    )
    db.session.add(issue)
    db.session.commit()

    logger.info("Issue created by user %s: %s", user_id, issue.title)
    return jsonify(IssueOut.from_orm(issue).dict()), 201


@bp.route("/issues", methods=["GET"])
@jwt_required()
def list_issues():
    issues = Issue.query.all()
    logger.debug("All issues fetched")
    return jsonify([issue.to_dict() for issue in issues]), 200


@bp.route("/issues/<int:issue_id>", methods=["GET"])
@jwt_required()
def get_issue(issue_id):
    issue = Issue.query.get_or_404(issue_id)
    logger.debug("Fetched issue %s", issue_id)
    return jsonify(issue.to_dict()), 200


@bp.route("/issues/<int:issue_id>", methods=["PUT"])
@jwt_required()
@owner_or_admin_required(Issue)
def update_issue(issue_id):
    issue = Issue.query.get_or_404(issue_id)
    try:
        update_data = IssueCreate(**request.get_json())
    except ValidationError as e:
        logger.warning("Invalid update input for issue %s", issue_id)
        return jsonify({"error": e.errors()}), 400

    issue.title = update_data.title
    issue.description = update_data.description
    db.session.commit()

    logger.info("Issue %s updated", issue_id)
    return jsonify(IssueOut.from_orm(issue).dict()), 200


@bp.route("/issues/<int:issue_id>", methods=["PATCH"])
@jwt_required()
@owner_or_admin_required(Issue)
def patch_issue(issue_id):
    issue = Issue.query.get_or_404(issue_id)
    data = request.get_json()
    if not data:
        logger.warning("Empty PATCH request on issue %s", issue_id)
        return jsonify({"error": "No input data provided"}), 400

    if "status" in data:
        issue.status = data["status"]
        db.session.commit()
        logger.info("Issue %s status updated to %s", issue_id, issue.status)

    return jsonify(issue.to_dict()), 200


@bp.route("/issues/<int:issue_id>", methods=["DELETE"])
@jwt_required()
@owner_or_admin_required(Issue)
def delete_issue(issue_id):
    issue = Issue.query.get_or_404(issue_id)
    db.session.delete(issue)
    db.session.commit()
    logger.info("Issue %s deleted", issue_id)
    return "", 204
