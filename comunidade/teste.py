from comunidade import app, database

# Criar banco de dados
# with app.app_context():
#     database.create_all()

# with app.app_context():
#     usuario = Usuario(username='Chad', email='merda@gmail.com', senha='123')
#     usuario_2 = Usuario(username='Chad2', email='kfdsd@dfskl.com', senha='123')
#
#     database.session.add(usuario)
#     database.session.add(usuario_2)
#
#     database.session.commit()

# with app.app_context():
#     meus_usuarios = Usuario.query.all()
#     print(meus_usuarios)
#
#     for usuario in meus_usuarios:
#         print(usuario.username)
#         print(usuario.email)
#         print(usuario.senha)
#         print(usuario.foto_perfil)
#         print(usuario.cursos)
#         print(usuario.posts)
#         print('-----------------')
#
#     query_usuario = Usuario.query.filter_by(id=1).first()
#     print(query_usuario.username)

# with app.app_context():
#     meu_post = Post(id=1, titulo='Titulo 1', corpo='Corpo 1', id_usuario=1)
#     meu_post_2 = Post(id=2, titulo='Titulo 2', corpo='Corpo 2', id_usuario=1)
#
#     database.session.add(meu_post)
#     database.session.add(meu_post_2)
#
#     database.session.commit()

# with app.app_context():
#     post = Post.query.first()
#     print(post.titulo)
#     print(post.autor.email)

with app.app_context():
    database.drop_all()
    database.create_all()