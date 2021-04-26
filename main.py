from flask import Flask, render_template, redirect, abort, request
from data import db_session
from data.users import User
from data.recipe import Recipe
from data.ingredient import Ingredient
from data.recipe_ingredients import RecipeIngredients
from forms.user import RegisterForm, LoginForm, IngredientFrom, New1Form, FilterForm
from forms.user import New2Form, New3Form, AddIngrToRecipe, StringField, ForNew2Form
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from PIL import Image


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")

        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            login=form.login.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()

        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/users/" + str(user.id))
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/users/<user_id>')
def user_page(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == user_id).first()
    date = str(user.date_reg.date())
    recipes = list(db_sess.query(Recipe).filter(Recipe.creator_id == user_id))
    id = str(db_sess.query(Recipe).count() + 1)
    return render_template('user.html',
                               user=user, date=date, recipes=recipes, id=id)


@app.route('/users')
def users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).filter(User.id <= 10)
    return render_template('users.html',
                               users=users)


@app.route('/ingredients', methods=['GET', 'POST'])
def ingr():
    db_sess = db_session.create_session()
    a = request.args.get('page')
    form = IngredientFrom()
    ingr = db_sess.query(Ingredient).filter(Ingredient.id <= 20)
    if a is not None and a.isdigit():
        k = db_sess.query(Ingredient).count() - 1
        if k < 0:
            k = 1
        page = k // 20 + 1
        a = int(a)
        if 1 <= a <= page:

            if form.validate_on_submit():
                if db_sess.query(Ingredient).filter(Ingredient.name == form.name.data).first():
                    return render_template('ingredients.html',
                                   ingr=ingr,
                                   form=form,
                                   message="Такой ингредиент уже есть",
                                   num=1)
                ing = Ingredient(name=form.name.data)
                db_sess.add(ing)
                db_sess.commit()
            ingr = db_sess.query(Ingredient).filter(Ingredient.id <= a * 20, Ingredient.id > (a - 1) * 20)
            return render_template('ingredients.html',
                                   ingr=ingr,
                                   form=form,
                                   num=a)
        else:
            return redirect('/ingredients?page=1')
    if form.validate_on_submit():
        if db_sess.query(Ingredient).filter(Ingredient.name == form.name.data).first():
            return render_template('ingredients.html',
                                   ingr=ingr,
                                   form=form,
                                   message="Такой ингредиент уже есть",
                                   num=1)
        ing = Ingredient(name=form.name.data)
        db_sess.add(ing)
        db_sess.commit()
    ingr = db_sess.query(Ingredient).filter(Ingredient.id <= 20)
    return render_template('ingredients.html', ingr=ingr, form=form, num=1)


@app.route('/new1', methods=['GET', 'POST'])
def new1():
    form = New1Form()
    a = request.args.get('id')
    db_sess = db_session.create_session()
    if a is None or int(a) != db_sess.query(Recipe).count() + 1 or not current_user.is_authenticated:
        abort(404)
    else:
        if form.validate_on_submit():
            recipe = Recipe(
                title=form.title.data,
                description=form.description.data,
                hard=form.hard.data,
                calorie=form.calorie.data,
                time=form.time.data,
                category=form.category.data,
                creator_id=current_user.id
            )
            db_sess.add(recipe)
            db_sess.commit()
            return redirect('/new2?id=' + str(a))
        return render_template('new1.html', form=form)


@app.route('/new2', methods=['GET', 'POST'])
def new2():
    form = New2Form()
    a = request.args.get('id')
    db_sess = db_session.create_session()
    if a is None or int(a) != db_sess.query(Recipe).count() or not current_user.is_authenticated or\
            current_user.id != db_sess.query(Recipe).filter(Recipe.id == int(a)).first().creator_id:
        abort(404)
    else:
        a = int(a)

        if form.validate_on_submit():
            recipe = db_sess.query(Recipe).filter(Recipe.id == a).first()
            for i in form.ingrs.data:
                recipe_ingr = db_sess.query(RecipeIngredients).join(Ingredient).filter(Ingredient.name == i["title"]).first()
                recipe_ingr.quantity = i['quantity']
                db_sess.commit()
            recipe.comment = form.comment.data
            db_sess.commit()
            return redirect('/new3?id=' + str(a))
        else:
            for i in db_sess.query(RecipeIngredients).filter(RecipeIngredients.recipe_id == a):
                ingr1 = ForNew2Form()
                ingr1.title = i.ingredient.name
                ingr1.quantity = ''
                form.ingrs.append_entry(ingr1)
        return render_template('new2.html', form=form, id=str(a))


@app.route('/add_ingr_to_recipe', methods=['GET', 'POST'])
def add_ingr_to_recipe():
    form = AddIngrToRecipe()
    a = request.args.get('id')
    b = request.args.get('query')
    db_sess = db_session.create_session()
    if a is None or int(a) != db_sess.query(Recipe).count() or not current_user.is_authenticated or\
            current_user.id != db_sess.query(Recipe).filter(Recipe.id == int(a)).first().creator_id:
        abort(404)
    else:
        if b is None:
            query1 = db_sess.query(Ingredient).order_by(Ingredient.name)
            form.choice.choices = [(g.id, g.name) for g in list(query1)]
        else:
            query1 = db_sess.query(Ingredient).filter(Ingredient.name.like('%' + b + '%')).order_by(Ingredient.name)
            form.choice.choices = [(g.id, g.name) for g in list(query1)]

        if form.validate_on_submit():
            if form.find.data:
                href = '/add_ingr_to_recipe?id=' + str(a) + '&query=' + form.search.data
                return redirect(href)

            if form.add_ingr.data:
                for id1 in form.choice.data:
                    print(id1)
                    if db_sess.query(RecipeIngredients).filter(RecipeIngredients.recipe_id == int(a),
                                                               RecipeIngredients.ingr_id == id1).first() is None:
                        ing1 = RecipeIngredients(
                            recipe_id=int(a),
                            ingr_id=id1
                        )
                        db_sess.add(ing1)
                        db_sess.commit()
                        ing2 = db_sess.query(Ingredient).filter(Ingredient.id == id1).first()
                        ing2.used = True
                        db_sess.commit()
                return redirect('/new2?id=' + str(a))
        return render_template('add_ingr_to_recipe.html', form=form, id=str(a))


@app.route('/new3', methods=['GET', 'POST'])
def new3():
    form = New3Form()
    a = request.args.get('id')
    db_sess = db_session.create_session()
    if a is None or int(a) != db_sess.query(Recipe).count() or not current_user.is_authenticated or\
            current_user.id != db_sess.query(Recipe).filter(Recipe.id == int(a)).first().creator_id:
        abort(404)
    else:
        if form.validate_on_submit():
            recipe = db_sess.query(Recipe).filter(Recipe.id == a).first()
            recipe.how_to = form.recipe_text.data
            db_sess.commit()
            user = current_user
            user.recipe_num = db_sess.query(Recipe).filter(Recipe.creator_id == current_user.id)
            db_sess.commit()
            if form.picture.data:
                form.picture.data.save('static/user_images/' + a + '.jpg')
            else:
                form.picture.data = Image.open('static/images/cooking.jpg')
                form.picture.data.save('static/user_images/' + a + '.jpg')
            return redirect('/users/' + str(current_user.id))
        return render_template('new3.html', form=form, id=str(a))


@app.route('/ing_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def ing_delete(id):
    db_sess = db_session.create_session()
    ing = db_sess.query(Ingredient).filter(Ingredient.id == id).first()
    if ing:
        db_sess.delete(ing)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/ingredients')


@app.route('/delete_from_recipe/<int:id>', methods=['GET', 'POST'])
@login_required
def ing_delete_from(id):
    db_sess = db_session.create_session()
    db_sess.query(RecipeIngredients).filter(RecipeIngredients.recipe_id == id).delete()
    db_sess.commit()
    return redirect('/new2?id=' + str(id))


@app.route('/')
def main_screen():
    categories = ['Мясные блюда', 'Выпечка', 'Супы', 'Напитки',
                  'Рыба и морепродукты', 'Каши', 'Закуски', 'Фастфуд',
                  'Гарниры', 'Салаты', 'Десерты', 'Другое']
    return render_template('main.html', cat=categories)


@app.route('/recipes', methods=['GET', 'POST'])
def show_recipes():
    form = FilterForm()
    db_sess = db_session.create_session()
    query1 = db_sess.query(Ingredient).filter(Ingredient.used == True).order_by(Ingredient.name)
    form.ingr_in.choices = [(g.id, g.name) for g in list(query1)]
    form.ingr_ex.choices = [(g.id, g.name) for g in list(query1)]
    cat = request.args.get('category')
    if cat is not None:
        recipes = db_sess.query(Recipe).filter(Recipe.category == cat)
    else:
        recipes = db_sess.query(Recipe)
    ingr_in = request.args.get('ingr_include')
    if ingr_in is not None:
        ingr_in = ingr_in.split(',')
        for i in ingr_in:
            recipes = recipes.join(RecipeIngredients).filter(RecipeIngredients.ingr_id == int(i))
    ingr_ex = request.args.get('ingr_exclude')
    if ingr_ex is not None:
        ingr_in = ingr_in.split(',')
        for i in ingr_in:
            recipes = recipes.join(RecipeIngredients).filter(RecipeIngredients.ingr_id != int(i))
    time = request.args.get('time')
    if time is not None:
        recipes = recipes.filter(Recipe.time <= int(time))
    calorie = request.args.get('calorie')
    if calorie is not None:
        recipes = recipes.filter(Recipe.calorie <= int(calorie))
    title = request.args.get('title')
    if title is not None:
        recipes = recipes.filter(Recipe.title.like('%' + title + '%'))
    user = request.args.get('user')
    if user is not None:
        recipes = recipes.filter(Recipe.creator_id.like('%' + user + '%'))
    sort = request.args.get('sort_by')
    if sort is not None:
        if sort == 'timeasc':
            recipes = recipes.order_by(Recipe.time)
        if sort == 'timedesc':
            recipes = recipes.order_by(Recipe.time.desc())
        if sort == 'titleasc':
            recipes = recipes.order_by(Recipe.title)
        if sort == 'titledesc':
            recipes = recipes.order_by(Recipe.title.desc())
        if sort == 'hardasc':
            recipes = recipes.order_by(Recipe.hard)
        if sort == 'harddesc':
            recipes = recipes.order_by(Recipe.hard.desc())
        if sort == 'dateasc':
            recipes = recipes.order_by(Recipe.date_publ)
        if sort == 'datedesc':
            recipes = recipes.order_by(Recipe.date_publ.desc())
    if form.validate_on_submit():
        a = list()
        a.append('category=' + form.category.data)
        if form.title.data:
            a.append('category=' + form.title.data)
        if form.time.data and form.time.data.isdigit():
            a.append('category=' + form.time.data)
        if form.calorie.data and form.calorie.data.isdigit():
            a.append('category=' + form.calorie.data)
        if form.sort_by.data == 'Дате публикации':
            m = 'date'
        elif form.sort_by.data == 'Времени приготовления':
            m = 'time'
        elif form.sort_by.data == 'Названию':
            m = 'title'
        else:
            m = 'hard'
        if form.sort_by2.data == 'В порядке возрастания':
            m += 'desc'
        else:
            m += 'asc'
        a.append('sort_by=' + m + '#showrecipes')
        if form.ingr_in.data:
            m1 = list()
            for i in form.ingr_in.data:
                m1.append(str(i))
            a.append('ingr_include=' + ','.join(m1))
        if form.ingr_ex.data:
            m1 = list()
            for i in form.ingr_ex.data:
                m1.append(str(i))
            a.append('ingr_exclude=' + ','.join(m1))
        return redirect('/recipes?' + '&'.join(a))
    return render_template('recipes.html', form=form, recipes=recipes)


@app.route('/recipes/<int:recipe_id>')
def recipe_alone(recipe_id):
    db_sess = db_session.create_session()
    recipe = db_sess.query(Recipe).filter(Recipe.id == recipe_id).first()
    ingredients = db_sess.query(RecipeIngredients).filter(RecipeIngredients.recipe_id == recipe_id).all()
    rec_text = recipe.how_to.split('\n')
    return render_template('recipe.html', recipe=recipe, ingredients=ingredients, rec_text=rec_text)


def main():
    db_session.global_init("db/recipe.db")
    app.run()


if __name__ == '__main__':
    main()
