from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .db import get_db
from .schemas import RecipeOut, RecipeCreate, RecipeUpdate
from .security import get_current_user
from .models import User, Recipe
from .repositories import (
    create_recipe as repo_create_recipe,
    list_recipes as repo_list_recipes,
    get_recipe as repo_get_recipe,
    update_recipe as repo_update_recipe,
    delete_recipe as repo_delete_recipe,
)

router = APIRouter(prefix="/recipes", tags=["recipes"])

@router.post("/", response_model=RecipeOut, summary="Create recipe", description="Create a new recipe owned by the current user.")
def create_recipe(payload: RecipeCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> Recipe:
    return repo_create_recipe(db, owner_id=current_user.id, title=payload.title, description=payload.description, ingredients=payload.ingredients, instructions=payload.instructions)


@router.get("/", response_model=List[RecipeOut], summary="List recipes", description="List recipes. If authenticated, returns all recipes; use query parameters in future for filtering.")
def list_recipes(db: Session = Depends(get_db)) -> list[Recipe]:
    return repo_list_recipes(db)


@router.get("/mine", response_model=List[RecipeOut], summary="List my recipes", description="List recipes owned by the current user.")
def list_my_recipes(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> list[Recipe]:
    return repo_list_recipes(db, owner_id=current_user.id)


@router.get("/{recipe_id}", response_model=RecipeOut, summary="Get recipe", description="Get a recipe by id.")
def get_recipe(recipe_id: int, db: Session = Depends(get_db)) -> Recipe:
    recipe = repo_get_recipe(db, recipe_id)
    if not recipe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
    return recipe


@router.patch("/{recipe_id}", response_model=RecipeOut, summary="Update recipe", description="Update a recipe owned by the current user.")
def update_recipe(recipe_id: int, payload: RecipeUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> Recipe:
    recipe = repo_get_recipe(db, recipe_id)
    if not recipe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
    if recipe.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to modify this recipe")
    updated = repo_update_recipe(db, recipe, title=payload.title, description=payload.description, ingredients=payload.ingredients, instructions=payload.instructions)
    return updated


@router.delete("/{recipe_id}", status_code=204, summary="Delete recipe", description="Delete a recipe owned by the current user.")
def delete_recipe(recipe_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    recipe = repo_get_recipe(db, recipe_id)
    if not recipe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
    if recipe.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this recipe")
    repo_delete_recipe(db, recipe)
    return None
