import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Ingredient(SqlAlchemyBase):
    __tablename__ = 'ingredient'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    used = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True, default=False)
    for_recipe = orm.relation("RecipeIngredients")