from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, BooleanField, Form
from wtforms.widgets import TextInput
from wtforms import IntegerField, FileField, SelectField, SelectMultipleField, FieldList, FormField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    login = StringField('Придумайте логин', validators=[DataRequired()])
    about = TextAreaField("Расскажите о себе")
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class IngredientFrom(FlaskForm):
    name = StringField('Название ингредиента/продукта', validators=[DataRequired()])
    submit = SubmitField('Добавить')


class New1Form(FlaskForm):
    choices = ['Мясные блюда', 'Выпечка', 'Супы', 'Напитки',
               'Рыба и морепродукты', 'Каши', 'Закуски', 'Фастфуд',
               'Гарниры', 'Салаты', 'Десерты', 'Другое']
    title = StringField('Название', validators=[DataRequired()])
    description = StringField('Краткое описание', validators=[DataRequired()])
    hard = IntegerField('Сложность; ../5', validators=[DataRequired()])
    calorie = IntegerField('Калорийность', validators=[DataRequired()])
    time = IntegerField('Общее время приготовления; мин', validators=[DataRequired()])
    category = SelectField('Выберите категорию', choices=choices, validators=[DataRequired()])
    submit = SubmitField('Далее')


class ForNew2Form(Form):
    quantity = StringField(validators=[DataRequired()])
    title = StringField()


class New2Form(FlaskForm):
    ingrs = FieldList(FormField(ForNew2Form))
    comment = TextAreaField('Комментарий к ингредиентам', validators=[DataRequired()])
    submit = SubmitField('Далее')


class AddIngrToRecipe(FlaskForm):
    add_ingr = SubmitField('Добавить выбранные ингридиенты')
    choice = SelectMultipleField(coerce=int)
    search = StringField('Введите название ингредиента: ')
    find = SubmitField('Искать')


class New3Form(FlaskForm):
    recipe_text = TextAreaField('Поэтапный рецепт', validators=[DataRequired()])
    picture = FileField('Картинка готового блюда', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Опубликовать')


class FilterForm(FlaskForm):
    choices = ['Мясные блюда', 'Выпечка', 'Супы', 'Напитки',
               'Рыба и морепродукты', 'Каши', 'Закуски', 'Фастфуд',
               'Гарниры', 'Салаты', 'Десерты', 'Другое']
    choices2 = ['Дате публикации', 'Времени приготовления', 'Названию', 'Сложности']
    category = SelectField('Категория', choices=choices)
    sort_by = SelectField('Сортировать по', choices=choices2)
    sort_by2 = SelectField(choices=['В порядке возрастания', 'В порядке убывания'])
    title = StringField('В названии есть')
    ingr_in = SelectMultipleField('С ингредиентами', coerce=int)
    ingr_ex = SelectMultipleField('Без ингредиентов', coerce=int)
    time = StringField('Время приготовление <=, мин')
    calorie = StringField('Калорийность <=, ккал')
    submit = SubmitField('Показать')