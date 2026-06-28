# api/auth_api.py
"""
Authentication API endpoints for the ATM Withdrawal System.

Provides RESTful endpoints for user login and logout.
Uses Flask-RESTful for resource routing and service-layer business logic.
"""

from flask import request
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError

from models import db
from services.auth_service import AuthService, AuthenticationError, AccountLockedError
from services.audit_service import AuditService
from utils import create_jwt_token

# Parser for login request
login_parser = reqparse.RequestParser()
login_parser.add_argument(
    'card_number',
    type=str,
    required=True,
    help='Card number is required.'
)
login_parser.add_argument(
    'pin',
    type=str,
    required=True,
    help='PIN is required.'
)


class AuthLogin(Resource):
    """
    Resource handling user authentication via card number and PIN.

    POST /auth/login
    """

    def post(self) -> tuple:
        """
        Authenticate a user and return a JWT access token.

        Request body (JSON):
            - card_number (str): The user's card number.
            - pin (str): The user's PIN.

        Responses:
            200: Authentication successful, returns {'token': <JWT>}.
            401: Invalid credentials (invalid card number or PIN).
            423: Account is locked due to too many failed attempts.
            500: Internal server error.
        """
        args = login_parser.parse_args()
        card_number = args['card_number'].strip()
        pin = args['pin']

        # Capture client IP for audit trail
        ip_address = request.remote_addr or '0.0.0.0'

        try:
            user = AuthService.authenticate(
                card_number=card_number,
                pin=pin,
                ip_address=ip_address
            )
            # Persist changes (reset failed attempts, audit logs, etc.)
            db.session.commit()
        except AccountLockedError as e:
            db.session.rollback()
            return {'error': str(e.message)}, 423
        except AuthenticationError as e:
            db.session.rollback()
            return {'error': str(e.message)}, 401
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'error': 'Database error during authentication'}, 500
        except Exception as e:
            db.session.rollback()
            # In production, log the actual exception
            return {'error': 'Internal server error'}, 500

        # Generate JWT token with user ID as identity
        token = create_jwt_token(
            identity=user.id,
            additional_claims={
                'card_number': user.card_number,  # optional, for later use
                'is_admin': False  # placeholder for admin differentiation
            }
        )

        # Return token
        return {'token': token}, 200


class AuthLogout(Resource):
    """
    Resource for logging out (invalidating the current token).

    POST /auth/logout
    This is a placeholder; actual token invalidation requires a blacklist.
    For simplicity, this endpoint just returns a success message.
    """

    @jwt_required()
    def post(self) -> tuple:
        """
        Log out the current user.

        In a production system, you would add the JWT's jti to a blacklist.
        Here we simply acknowledge the request.

        Responses:
            200: Logout acknowledged.
            500: Internal server error.
        """
        user_id = get_jwt_identity()
        try:
            AuditService.log_action(
                action='LOGOUT',
                user_id=user_id,
                transaction_id=None,
                details='User logged out.'
            )
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            return {'error': 'Failed to log logout action'}, 500
        except Exception:
            db.session.rollback()
            return {'error': 'Internal server error'}, 500

        return {'message': 'Logout successful'}, 200
