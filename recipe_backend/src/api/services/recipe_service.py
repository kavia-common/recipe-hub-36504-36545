from typing import List, Optional
from sqlalchemy.orm import Session

from ..models import Recipe, User
from ..repositories import (
    create_recipe as repo_create_recipe,
    list_recipes as repo_list_recipes,
    get_recipe as repo_get_recipe,
    update_recipe as repo_update_recipe,
    delete_recipe as repo_delete_recipe,
)


# PUBLIC_INTERFACE
def create_user_recipe(
    db: Session,
    owner: User,
    title: str,
    description: Optional[str] = None,
    ingredients: Optional[str] = None,
    instructions: Optional[str] = None,
) -> Recipe:
    """Create a new recipe owned by the specified user."""
    return repo_create_recipe(
        db=db,
        owner_id=owner.id,
        title=title,
        description=description,
        ingredients=ingredients,
        instructions=instructions,
    )


# PUBLIC_INTERFACE
def get_recipe_or_404(db: Session, recipe_id: int) -> Optional[Recipe]:
    """Return recipe or None if missing."""
    return repo_get_recipe(db, recipe_id)


# PUBLIC_INTERFACE
def ensure_owner(recipe: Recipe, user: User) -> bool:
    """Check if the given user owns the recipe."""
    return recipe.owner_id == user.id


# PUBLIC_INTERFACE
def list_all_recipes(db: Session) -> List[Recipe]:
    """List all recipes."""
    return repo_list_recipes(db)


# PUBLIC_INTERFACE
def list_user_recipes(db: Session, user: User) -> List[Recipe]:
    """List recipes owned by the given user."""
    return repo_list_recipes(db, owner_id=user.id)


# PUBLIC_INTERFACE
def update_user_recipe(
    db: Session,
    recipe: Recipe,
    *,
    title: Optional[str] = None,
    description: Optional[str] = None,
    ingredients: Optional[str] = None,
    instructions: Optional[str] = None,
) -> Recipe:
    """Update fields of a recipe."""
    return repo_update_recipe(
        db,
        recipe,
        title=title,
        description=description,
        ingredients=ingredients,
        instructions=instructions,
    )


# PUBLIC_INTERFACE
def delete_user_recipe(db: Session, recipe: Recipe) -> None:
    """Delete the recipe."""
    repo_delete_recipe(db, recipe)
