"""
users/services.py - Re-exports Codeforces API client & synchronization services
from the dedicated codeforces app for modularity and backwards compatibility.
"""

from codeforces.services import (
    call_codeforces_api,
    sync_user_codeforces,
    get_cf_rank_info,
)

__all__ = [
    'call_codeforces_api',
    'sync_user_codeforces',
    'get_cf_rank_info',
]
