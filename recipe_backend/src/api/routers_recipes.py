from typing import Any, Dict
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from .db import get_db
from .schemas import RecipeOut, RecipeCreate, RecipeUpdate
from .models import User, Recipe
from .dependencies.auth import current_user, recipe_owned_by_current_user
from .services.recipe_service import (
    create_user_recipe,
    list_all_recipes,
    list_user_recipes,
    get_recipe_or_404,
    update_user_recipe,
    delete_user_recipe,
)
from .utils.pagination import paginate_items

router = APIRouter(prefix="/recipes", tags=["recipes"])

@router.post("/", response_model=RecipeOut, summary="Create recipe", description="Create a new recipe owned by the current user.")
def create_recipe(payload: RecipeCreate, db: Session = Depends(get_db), user: User = Depends(current_user)) -> Recipe:
    return create_user_recipe(
        db,
        owner=user,
        title=payload.title,
        description=payload.description,
        ingredients=payload.ingredients,
        instructions=payload.instructions,
    )


@router.get(
    "/",
    summary="List recipes",
    description="List all recipes with simple pagination.",
    response_description="Paginated list of recipes",
)
def list_recipes(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="1-based page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
) -> Dict[str, Any]:
    items = list_all_recipes(db)
    return paginate_items(items, page=page, page_size=page_size)


@router.get(
    "/mine",
    summary="List my recipes",
    description="List recipes owned by the current user with simple pagination.",
    response_description="Paginated list of recipes owned by the current user",
)
def list_my_recipes(
    db: Session = Depends(get_db),
    user: User = Depends(current_user),
    page: int = Query(1, ge=1, description="1-based page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
) -> Dict[str, Any]:
    items = list_user_recipes(db, user)
    return paginate_items(items, page=page, page_size=page_size)


@router.get("/{recipe_id}", response_model=RecipeOut, summary="Get recipe", description="Get a recipe by id.")
def get_recipe(recipe_id: int, db: Session = Depends(get_db)) -> Recipe:
    recipe = get_recipe_or_404(db, recipe_id)
    if not recipe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
    return recipe


@router.patch("/{recipe_id}", response_model=RecipeOut, summary="Update recipe", description="Update a recipe owned by the current user.")
def update_recipe(
    recipe_id: int,
    payload: RecipeUpdate,
    db: Session = Depends(get_db),
    recipe: Recipe = Depends(recipe_owned_by_current_user),
) -> Recipe:
    updated = update_user_recipe(
        db,
        recipe,
        title=payload.title,
        description=payload.description,
        ingredients=payload.ingredients,
        instructions=payload.instructions,
    )
    return updated


@router.delete("/{recipe_id}", status_code=204, summary="Delete recipe", description="Delete a recipe owned by the current user.")
def delete_recipe(
    recipe_id: int,
    db: Session = Depends(get_db),
    recipe: Recipe = Depends(recipe_owned_by_current_user),
):
    delete_user_recipe(db, recipe)
    return None
