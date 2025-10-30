from typing import Any, Dict, List, Sequence, TypeVar

T = TypeVar("T")

# PUBLIC_INTERFACE
def paginate_items(
    items: Sequence[T] | List[T],
    page: int = 1,
    page_size: int = 10,
) -> Dict[str, Any]:
    """Return a paginated payload for a sequence of items.

    The result format is:
    {
        "items": [...],
        "total": <int>,
        "page": <int>,
        "page_size": <int>
    }

    This is a simple, in-memory pagination helper suitable for small datasets
    or after a repository/service already applied DB-level pagination.

    Args:
        items: A sequence of items already materialized (e.g. list of ORM models or DTOs).
        page: 1-based page index. Invalid values are clamped to a minimum of 1.
        page_size: Number of items per page. Invalid values are clamped to a minimum of 1.

    Returns:
        A dict with items slice and metadata total, page, page_size.

    Notes:
        - This is intentionally minimal; for large datasets, prefer DB-level LIMIT/OFFSET.
        - If page is beyond the total range, an empty list will be returned for "items".
    """
    # Normalize inputs
    safe_page = max(1, int(page or 1))
    safe_page_size = max(1, int(page_size or 10))

    total = len(items)
    start = (safe_page - 1) * safe_page_size
    end = start + safe_page_size
    sliced = list(items[start:end]) if start < total else []

    return {
        "items": sliced,
        "total": total,
        "page": safe_page,
        "page_size": safe_page_size,
    }
