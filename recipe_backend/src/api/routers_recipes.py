from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
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


@router.get("/", response_model=List[RecipeOut], summary="List recipes", description="List all recipes.")
def list_recipes(db: Session = Depends(get_db)) -> list[Recipe]:
    return list_all_recipes(db)


@router.get("/mine", response_model=List[RecipeOut], summary="List my recipes", description="List recipes owned by the current user.")
def list_my_recipes(db: Session = Depends(get_db), user: User = Depends(current_user)) -> list[Recipe]:
    return list_user_recipes(db, user)


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
