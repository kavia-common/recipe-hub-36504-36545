from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import User, Recipe
from ..security import get_current_user
from ..services.recipe_service import ensure_owner, get_recipe_or_404


# PUBLIC_INTERFACE
def current_user(
    db: Session = Depends(get_db),
    token_user: User = Depends(get_current_user),
) -> User:
    """Alias dependency to retrieve the currently authenticated user.

    This wraps security.get_current_user to provide a single import path for
    dependencies and to make it easy to swap implementations in the future.
    """
    # Return the user extracted by the underlying security dependency
    return token_user


# PUBLIC_INTERFACE
def recipe_owned_by_current_user(
    recipe_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(current_user),
) -> Recipe:
    """Dependency ensuring the recipe exists and is owned by the current user.

    Raises:
        HTTPException 404: If the recipe does not exist.
        HTTPException 403: If the recipe is not owned by the authenticated user.
    """
    recipe = get_recipe_or_404(db, recipe_id)
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found"
        )
    if not ensure_owner(recipe, user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized for this recipe",
        )
    return recipe
