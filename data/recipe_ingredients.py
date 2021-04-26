import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class RecipeIngredients(SqlAlchemyBase):
    __tablename__ = 'recipe_ingrs'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    ingr_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("ingredient.id"), nullable=True)
    recipe_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("recipe.id"), nullable=True)
    quantity = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    recipe = orm.relation("Recipe", back_populates='ingredients')
    ingredient = orm.relation("Ingredient", back_populates='for_recipe')
