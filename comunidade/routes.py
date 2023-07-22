from flask import render_template, flash, redirect, url_for, request, abort
from comunidade.forms import FormLogin, FormCriarConta, FormEditarPerfil, FormCriarPost, ValidationError
from comunidade import app, database, bcrypt
from comunidade.models import Usuario, Post
from flask_login import login_user, current_user, logout_user, login_required
from comunidade.ultis.salvar_imagem import salvar_imagem
from comunidade.ultis.atualizar_cursos import atualizar_curso
from flask_wtf.csrf import generate_csrf


@app.route("/", endpoint='home')
def hello_world():

    posts = Post.query.order_by(Post.id.desc()).all()

    return render_template("index.html", posts=posts)


@app.route("/contatos")
def contatos():
    return render_template('contato.html')


@app.route("/usuarios/", endpoint="usuarios")
@login_required
def usuarios():

    lista_usuarios = Usuario.query.all()

    return render_template('usuarios.html', lista_usuarios=lista_usuarios)


@app.route('/login', methods=['GET', 'POST'], endpoint='login')
def login():
    form_login = FormLogin()
    form_criar_conta = FormCriarConta()

    if form_login.validate_on_submit() and 'submit_login' in request.form:

        usuario = Usuario.query.filter_by(email=form_login.email_login.data).first()

        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha_login.data):
            login_user(usuario, remember=form_login.lembrar.data)
            flash(f'Login realizado com sucesso! {current_user.username}', 'success')
            param_next = request.args.get('next')
            return redirect(param_next) if param_next else redirect(url_for('home'))
        else:
            flash('Login não realizado. Verifique email e senha.', 'danger')

    if form_criar_conta.validate_on_submit() and 'submit_criar_conta' in request.form:

        senha_criptografada = bcrypt.generate_password_hash(form_criar_conta.senha.data).decode('utf-8')

        usuario = Usuario(
            username=form_criar_conta.username.data,
            email=form_criar_conta.email.data,
            senha=senha_criptografada
        )

        database.session.add(usuario)
        database.session.commit()

        flash(f'Conta criada com sucesso! {form_criar_conta.username.data}', 'success')
        return redirect(url_for('home'))

    return render_template('login.html', form_login=form_login, form_criar_conta=form_criar_conta)


@app.route('/sair', endpoint='sair')
@login_required
def sair():
    logout_user()
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('home'))


@app.route('/perfil', endpoint='perfil')
@login_required
def perfil():

    foto_perfil = url_for('static', filename='fotos_perfil/' + current_user.foto_perfil)

    return render_template('perfil.html', foto_perfil=foto_perfil)


@app.route('/perfil/editar', methods=['GET', 'POST'], endpoint='perfil_editar')
@login_required
def perfil_editar():

    usuario = Usuario.query.filter_by(username=current_user.username).first()
    foto_perfil = url_for('static', filename='fotos_perfil/' + current_user.foto_perfil)
    form_editar_perfil = FormEditarPerfil()

    if form_editar_perfil.validate_on_submit():
        current_user.username = form_editar_perfil.username.data
        current_user.email = form_editar_perfil.email.data

        if form_editar_perfil.foto_perfil.data:
            nome_imagem = salvar_imagem(form_editar_perfil.foto_perfil.data)
            current_user.foto_perfil = nome_imagem

        current_user.cursos = atualizar_curso(form_editar_perfil)

        database.session.commit()
        flash('Perfil atualizado com sucesso!', 'success')
        return redirect(url_for('perfil'))

    elif request.method == 'GET':
        form_editar_perfil.username.data = current_user.username
        form_editar_perfil.email.data = current_user.email

    return render_template('perfil_editar.html', foto_perfil=foto_perfil, form_editar_perfil=form_editar_perfil, usuario=usuario)


@app.route('/post/create', methods=['GET', 'POST'], endpoint='post_create')
@login_required
def post_create():

    form = FormCriarPost()

    if form.validate_on_submit():
        post = Post(titulo=form.titulo.data,
             corpo=form.corpo.data,
             autor=current_user)
        database.session.add(post)
        database.session.commit()
        flash('Post criado com sucesso!', 'success')
        return redirect(url_for('home'))

    return render_template('post_create.html', form=form)


@app.route('/post/<int:post_id>', endpoint='post', methods=['GET', 'POST'])
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)

    csrf_token = generate_csrf()

    if current_user == post.autor:
        form = FormCriarPost()
        if request.method == 'GET':
            form.titulo.data = post.titulo
            form.corpo.data = post.corpo
        elif form.validate_on_submit():
            post.titulo = form.titulo.data
            post.corpo = form.corpo.data
            database.session.commit()
            flash('Post atualizado com sucesso!', 'success')
            return redirect(url_for('post', post_id=post.id))
    else:
        form = None

    return render_template('post.html', post=post, form=form, csrf_token=csrf_token)


@app.route('/post/<int:post_id>/delete', endpoint='post_delete', methods=['POST', 'GET'])
def post_delete(post_id):

    post = Post.query.get_or_404(post_id)

    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        flash('Post deletado com sucesso!', 'success')
        return redirect(url_for('home'))
    else:
        abort(403)
        flash('Você não tem permissão para deletar esse post!', 'danger')
        return redirect(url_for('home'))