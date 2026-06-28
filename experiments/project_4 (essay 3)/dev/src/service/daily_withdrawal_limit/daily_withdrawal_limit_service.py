from __future__ import annotations

from typing import Any

"""
Service layer for the DailyWithdrawalLimit domain class

Package: service.daily_withdrawal_limit
Layer: service
Related tasks: #97, #98
Requirement coverage:
- Decline Withdrawals Exceeding Account Balance or Daily Limit
- Atomic Withdrawal Transactions
"""

class REQ_BAL_01:
    def __init__(self, initiator: "oneActor | None" = None, target: "someResource | None" = None, channel: "someInterface | None" = None, grant: "onePermission | None" = None, pre: "oneState | None" = None, post: "oneState | None" = None, invariant_1: "inv_operation_requires_channel:somechannel | None" = None, invariant_2: "inv_operation_requires_target:sometarget | None" = None, invariant_3: "inv_initiator_is_authorized:grantininitiator.mayPerform | None" = None, invariant_4: "inv_resource_access_control:initiatorintarget.accessible | None" = None, invariant_5: "inv_state_must_change:pre!=post | None" = None, invariant_6: "inv_authenticated_channel_required:somec:channel|c.authenticated=True | None" = None, invariant_7: "postconditions_must_reach_defined_states:postinPost1 | None" = None, invariant_8: "nfr_fact_usability_interface_limit:#channel<=3 | None" = None, invariant_9: "nfr_fact_usability_single_initiator:oneinitiator | None" = None, invariant_10: "alldisjc1,c2:channel|c1.kind!=c2.kind | None" = None) -> None:
        self.initiator = initiator
        self.target = target
        self.channel = channel
        self.grant = grant
        self.pre = pre
        self.post = post
        self.invariant_1 = invariant_1
        self.invariant_2 = invariant_2
        self.invariant_3 = invariant_3
        self.invariant_4 = invariant_4
        self.invariant_5 = invariant_5
        self.invariant_6 = invariant_6
        self.invariant_7 = invariant_7
        self.invariant_8 = invariant_8
        self.invariant_9 = invariant_9
        self.invariant_10 = invariant_10