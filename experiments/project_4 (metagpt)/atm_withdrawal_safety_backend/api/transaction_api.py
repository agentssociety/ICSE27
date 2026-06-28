# api/transaction_api.py
"""
Transaction API endpoints for the ATM Withdrawal System.

Provides RESTful endpoints for processing withdrawals and retrieving
transaction history. All endpoints require JWT authentication.
"""

from typing import Optional

from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError

from models import db, User, Transaction
from services.transaction_service import TransactionService
from utils import get_current_user_id, validate_positive_decimal

# Parser for withdrawal request
withdrawal_parser = reqparse.RequestParser()
withdrawal_parser.add_argument(
    'amount',
    type=float,
    required=True,
    help='Amount to withdraw (positive number with up to 2 decimal places) is required.'
)


class Withdrawal(Resource):
    """
    Resource for processing a withdrawal transaction.

    POST /withdraw
    Requires a valid JWT token in the Authorization header.
    """

    @jwt_required()
    def post(self) -> tuple:
        """
        Process a withdrawal for the authenticated user.

        Request body (JSON):
            - amount (float): The amount to withdraw.

        Responses:
            200: Withdrawal successful, returns { 'transaction_id': <int> }.
            400: Invalid amount or exceeds limits (returns error message).
            401: Unauthorized (invalid/expired token).
            500: Internal server error.
        """
        # Parse and validate the request
        args = withdrawal_parser.parse_args()
        amount_raw = args['amount']

        # Validate that amount is a positive Decimal with ≤2 decimal places
        try:
            amount = validate_positive_decimal(amount_raw)
        except (ValueError, TypeError) as ve:
            return {'error': str(ve)}, 400

        # Retrieve the current user from the JWT identity
        user_id = get_current_user_id()
        user: Optional[User] = User.query.get(user_id)

        if not user:
            return {'error': 'User not found.'}, 401

        # Ensure the user account is not locked
        if user.is_locked:
            return {'error': 'Account is locked. Cannot perform withdrawals.'}, 403

        # Process the withdrawal via the service layer
        try:
            result = TransactionService.process_withdrawal(user, amount)

            if result['success']:
                # Service already committed; no need to commit again
                return {
                    'transaction_id': result['transaction_id'],
                    'message': 'Withdrawal successful.'
                }, 200
            else:
                db.session.rollback()
                return {'error': result['error']}, 400

        except SQLAlchemyError:
            db.session.rollback()
            return {'error': 'Database error during withdrawal.'}, 500
        except Exception:
            db.session.rollback()
            return {'error': 'Internal server error.'}, 500


class TransactionHistory(Resource):
    """
    Resource for retrieving the transaction history of the authenticated user.

    GET /history
    Requires a valid JWT token.
    """

    @jwt_required()
    def get(self) -> tuple:
        """
        Return a list of all transactions for the authenticated user.

        Responses:
            200: Returns a JSON list of transactions.
            401: Unauthorized (invalid/expired token).
            500: Internal server error.
        """
        user_id = get_current_user_id()
        user: Optional[User] = User.query.get(user_id)

        if not user:
            return {'error': 'User not found.'}, 401

        try:
            transactions = Transaction.query.filter_by(user_id=user_id)\
                .order_by(Transaction.timestamp.desc())\
                .all()

            # Serialize transactions into a list of dictionaries
            history = []
            for tx in transactions:
                history.append({
                    'transaction_id': tx.id,
                    'amount': float(tx.amount),
                    'timestamp': tx.timestamp.isoformat(),
                    'status': tx.status,
                    'decline_reason': tx.decline_reason,
                    'is_flagged': tx.is_flagged
                })

            return {'transactions': history}, 200

        except SQLAlchemyError:
            return {'error': 'Database error while fetching transaction history.'}, 500
        except Exception:
            return {'error': 'Internal server error.'}, 500
