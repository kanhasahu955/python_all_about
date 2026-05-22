"""Shared pagination limits for list endpoints."""

DEFAULT_PAGE_LIMIT = 20
MAX_PAGE_LIMIT = 100


def clamp_limit(limit: int) -> int:
    return max(1, min(limit, MAX_PAGE_LIMIT))
