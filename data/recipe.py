import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Recipe(SqlAlchemyBase):
    __tablename__ = 'recipe'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    category = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    calorie = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    time = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    hard = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    creator_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    date_publ = sqlalchemy.Column(sqlalchemy.DateTime,
                                  default=datetime.datetime.now)
    comment = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    how_to = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    user = orm.relation('User')
    ingredients = orm.relation('RecipeIngredients')