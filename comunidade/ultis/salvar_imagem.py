from PIL import Image
import secrets
import os

from comunidade import app


def salvar_imagem(imagem):
    token = secrets.token_hex(8)
    nome, extensao = os.path.splitext(imagem.filename)
    nome_imagem = nome + token + extensao
    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_imagem)

    tamanho = (200, 200)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    imagem_reduzida.save(caminho_completo)

    return nome_imagem