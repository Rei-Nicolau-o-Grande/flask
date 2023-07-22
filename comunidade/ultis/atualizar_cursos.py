

def atualizar_curso(form):
    lista_cursos = []
    for campo in form:
        if campo.name.startswith('curso_') and campo.data:
            lista_cursos.append(campo.label.text)
    return ';'.join(lista_cursos)