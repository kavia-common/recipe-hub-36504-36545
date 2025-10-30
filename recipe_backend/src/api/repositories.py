from typing import Optional, List
from sqlalchemy.orm import Session
from .models import User, Recipe
from .security import hash_password

# PUBLIC_INTERFACE
def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get a user by email."""
    return db.query(User).filter(User.email == email).first()


# PUBLIC_INTERFACE
def create_user(db: Session, email: str, password: str, full_name: Optional[str] = None) -> User:
    """Create a new user with hashed password."""
    user = User(email=email, hashed_password=hash_password(password, email), full_name=full_name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# PUBLIC_INTERFACE
def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """Validate user credentials."""
    user = get_user_by_email(db, email)
    if not user:
        return None
    if user.hashed_password != hash_password(password, email):
        return None
    return user


# PUBLIC_INTERFACE
def list_users(db: Session) -> List[User]:
    """List all users."""
    return db.query(User).order_by(User.id.desc()).all()


# PUBLIC_INTERFACE
def update_user(db: Session, user: User, full_name: Optional[str] = None, password: Optional[str] = None) -> User:
    """Update user details and/or password."""
    if full_name is not None:
        user.full_name = full_name
    if password:
        user.hashed_password = hash_password(password, user.email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# PUBLIC_INTERFACE
def delete_user(db: Session, user: User) -> None:
    """Delete a user."""
    db.delete(user)
    db.commit()


# RECIPES

# PUBLIC_INTERFACE
def create_recipe(db: Session, owner_id: int, title: str, description: str = None, ingredients: str = None, instructions: str = None) -> Recipe:
    """Create a recipe for an owner."""
    recipe = Recipe(owner_id=owner_id, title=title, description=description, ingredients=ingredients, instructions=instructions)
    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    return recipe


# PUBLIC_INTERFACE
def get_recipe(db: Session, recipe_id: int) -> Optional[Recipe]:
    """Get a recipe by id."""
    return db.query(Recipe).filter(Recipe.id == recipe_id).first()


# PUBLIC_INTERFACE
def list_recipes(db: Session, owner_id: Optional[int] = None) -> List[Recipe]:
    """List recipes; optionally filtered by owner."""
    q = db.query(Recipe)
    if owner_id is not None:
        q = q.filter(Recipe.owner_id == owner_id)
    return q.order_by(Recipe.id.desc()).all()


# PUBLIC_INTERFACE
def update_recipe(db: Session, recipe: Recipe, **fields) -> Recipe:
    """Patch a recipe."""
    for k, v in fields.items():
        if v is not None and hasattr(recipe, k):
            setattr(recipe, k, v)
    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    return recipe


# PUBLIC_INTERFACE
def delete_recipe(db: Session, recipe: Recipe) -> None:
    """Delete a recipe."""
    db.delete(recipe)
    db.commit()
