"""
Admin API endpoints for the ATM Withdrawal System.

Provides RESTful endpoints for administrative operations:
- Viewing flagged transactions
- Reviewing flagged transactions
- Locking/unlocking user accounts

All endpoints require JWT authentication with admin privileges.
"""

from typing import Optional, Tuple

from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt_claims
from sqlalchemy.exc import SQLAlchemyError

from models import db, FlaggedTransaction
from services.admin_service import AdminService
from services.fraud_service import FraudDetectionService
from services.audit_service import AuditService


def admin_required() -> None:
    """
    Check that the current JWT token has admin privileges.

    Raises:
        PermissionError: If the user is not an admin.
    """
    claims = get_jwt_claims()
    if not claims.get('is_admin', False):
        raise PermissionError("Admin privileges required.")


# ---------- Request Parsers ----------

flagged_list_parser = reqparse.RequestParser()
flagged_list_parser.add_argument(
    'review_status',
    type=str,
    required=False,
    help='Optional filter: pending, approved, declined',
    location='args'
)

review_parser = reqparse.RequestParser()
review_parser.add_argument(
    'flagged_id',
    type=int,
    required=True,
    help='ID of the flagged transaction is required.'
)
review_parser.add_argument(
    'status',
    type=str,
    required=True,
    choices=['approved', 'declined'],
    help='Review status must be "approved" or "declined".'
)

account_lock_parser = reqparse.RequestParser()
account_lock_parser.add_argument(
    'user_id',
    type=int,
    required=True,
    help='User ID is required.'
)
account_lock_parser.add_argument(
    'lock',
    type=bool,
    required=True,
    help='Lock (true) or unlock (false) is required.'
)


# ---------- Resource Classes ----------

class FlaggedList(Resource):
    """
    Resource for listing all flagged transactions.

    GET /admin/flagged
    Requires JWT token with admin privileges.
    """

    @jwt_required()
    def get(self) -> Tuple[dict, int]:
        """
        Return all flagged transactions, optionally filtered by review_status.

        Query parameters:
            review_status (str, optional): Filter by status (pending, approved, declined).

        Responses:
            200: JSON list of flagged transactions.
            403: Forbidden (non-admin user).
            500: Internal server error.
        """
        try:
            admin_required()
        except PermissionError as e:
            return {'error': str(e)}, 403

        args = flagged_list_parser.parse_args()
        review_status = args.get('review_status')

        try:
            flagged_transactions = FraudDetectionService.get_flagged_transactions(
                review_status=review_status
            )
        except SQLAlchemyError:
            return {'error': 'Database error while fetching flagged transactions.'}, 500
        except Exception:
            return {'error': 'Internal server error.'}, 500

        # Serialize
        result = []
        for ft in flagged_transactions:
            transaction = ft.transaction
            result.append({
                'flagged_id': ft.id,
                'transaction_id': transaction.id,
                'user_id': transaction.user_id,
                'amount': float(transaction.amount),
                'timestamp': transaction.timestamp.isoformat(),
                'reason': ft.reason,
                'severity': ft.severity,
                'review_status': ft.review_status,
                'reviewed_by': ft.reviewed_by,
                'review_timestamp': ft.review_timestamp.isoformat() if ft.review_timestamp else None
            })

        return {'flagged_transactions': result}, 200


class ReviewFlagged(Resource):
    """
    Resource for reviewing a flagged transaction.

    POST /admin/review
    Requires JWT token with admin privileges.
    """

    @jwt_required()
    def post(self) -> Tuple[dict, int]:
        """
        Update the review status of a flagged transaction.

        Request body (JSON):
            flagged_id (int): ID of the flagged transaction.
            status (str): New status, either "approved" or "declined".

        Responses:
            200: Review status updated successfully.
            400: Invalid input (e.g., invalid flagged_id or status).
            403: Forbidden (non-admin user).
            500: Internal server error.
        """
        try:
            admin_required()
        except PermissionError as e:
            return {'error': str(e)}, 403

        args = review_parser.parse_args()
        flagged_id = args['flagged_id']
        status = args['status']

        reviewer_id = get_jwt_identity()

        try:
            AdminService.review_flagged_transaction(
                flagged_id=flagged_id,
                reviewer_id=reviewer_id,
                status=status
            )
            db.session.commit()
        except ValueError as e:
            db.session.rollback()
            return {'error': str(e)}, 400
        except SQLAlchemyError:
            db.session.rollback()
            return {'error': 'Database error during review.'}, 500
        except Exception:
            db.session.rollback()
            return {'error': 'Internal server error.'}, 500

        return {'message': f'Flagged transaction {flagged_id} reviewed as {status}.'}, 200


class AccountLock(Resource):
    """
    Resource for locking or unlocking a user account.

    POST /admin/account/lock
    Requires JWT token with admin privileges.
    """

    @jwt_required()
    def post(self) -> Tuple[dict, int]:
        """
        Lock or unlock a user account.

        Request body (JSON):
            user_id (int): ID of the user.
            lock (bool): True to lock, False to unlock.

        Responses:
            200: Account lock status changed.
            400: Invalid user ID.
            403: Forbidden (non-admin user).
            500: Internal server error.
        """
        try:
            admin_required()
        except PermissionError as e:
            return {'error': str(e)}, 403

        args = account_lock_parser.parse_args()
        user_id = args['user_id']
        lock = args['lock']

        try:
            AdminService.lock_unlock_account(user_id=user_id, lock=lock)
            db.session.commit()
        except ValueError as e:
            db.session.rollback()
            return {'error': str(e)}, 400
        except SQLAlchemyError:
            db.session.rollback()
            return {'error': 'Database error during account lock/unlock.'}, 500
        except Exception:
            db.session.rollback()
            return {'error': 'Internal server error.'}, 500

        action = 'locked' if lock else 'unlocked'
        return {'message': f'Account for user {user_id} has been {action}.'}, 200
