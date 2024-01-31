from flask import Flask, jsonify, request, make_response
from estrutura_banco_de_dados import Postagem, Autor, app, db
import jwt
from datetime import datetime, timedelta
from functools import wraps

def validar_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # verificar se um token foi enviado
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'mensagem':'O token não foi incluído'}, 401)
        # se temos um token, validar usando o bd
        try:
            resultado = jwt.decode(
                token, app.config['SECRET_KEY'], algorithms=['HS256'])
            autor = Autor.query.filter_by(id_autor=resultado['id_autor']).first()
        except:
            return jsonify({'Mensagem':'Token inválido.'}, 401)
        return f(autor, *args, **kwargs)
    return decorated

@app.route('/login')
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response(
            'login inválido', 401, {'WWW-Authenticate': 'Basic realm="Login Obrigatório"'})
    usuario = Autor.query.filter_by(nome=auth.username).first()
    
    if not usuario:
        return make_response(
            'login inválido', 401, {'WWW-Authenticate': 'Basic realm="Login Obrigatório"'})
    
    if auth.password != usuario.senha:
        return make_response(
            'login inválido', 401, {'WWW-Authenticate': 'Basic realm="Login Obrigatório"'})
    
    if auth.password == usuario.senha:
        token = jwt.encode(
            {'id_autor': usuario.id_autor, 'exp': datetime.utcnow() + timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'token': token})

# http://localhost:5000
@app.route('/postagens')
# @validar_token
def obter_postagens():
    postagens = Postagem.query.all()
    lista_de_postagens = []
    for postagem in postagens:
        postagem_atual={}
        postagem_atual['id_postagem'] = postagem.id_postagem
        postagem_atual['titulo'] = postagem.titulo
        postagem_atual['id_autor'] = postagem.id_autor
        lista_de_postagens.append(postagem_atual)
    
    return jsonify({'postagens': lista_de_postagens})
        
# http://localhost:5000/postagem/[indice]

@app.route('/postagem/<int:id_postagem>',methods=['GET'])
# @validar_token
def obter_postagem_por_id(id_postagem):
    postagem = Postagem.query.filter_by(id_postagem=id_postagem).first()
    if not postagem:
        return jsonify({'mensagem': 'Postagem não encontrada.'}, 404)
    postagem_atual = {}
    postagem_atual['id_postagem'] = postagem.id_postagem
    postagem_atual['titulo'] = postagem.titulo
    postagem_atual['id_autor'] = postagem.id_autor
    
    return jsonify({'Postagem': postagem_atual})
    
# http://localhost:5000/postagem
@app.route('/postagem',methods=['POST'])
@validar_token
def adicionar_postagem(autor):
    nova_postagem = request.get_json()
    postagem = Postagem(titulo=nova_postagem['titulo'], id_autor=nova_postagem['id_autor'])
    
    db.session.add(postagem)
    db.session.commit()

    return jsonify({'Postagem adicionada': nova_postagem}, 200)
# http://localhost:5000/postagem/[indice]
@app.route('/postagem/<int:id_postagem>',methods=['PUT'])
@validar_token
def alterar_postagem(autor, id_postagem):
    postagem_a_alterar = request.get_json()
    postagem = Postagem.query.filter_by(id_postagem=id_postagem).first()
    try:
        if not postagem:
            return jsonify({'mensagem': 'Postagem não encontrada.'}, 404)
    except:
        pass

    try:
        postagem.titulo = postagem_a_alterar['titulo']
    except:
        pass

    try:
        postagem.id_autor = postagem_a_alterar['id_autor']
    except:
        pass
    
    db.session.commit()
    
    return jsonify({'alteração feita com sucesso': postagem_a_alterar}, 200)
# http://localhost:5000/postagem/[indice]
@app.route('/postagem/<int:id_postagem>', methods=['DELETE'])
@validar_token
def deletar_postagem(autor, id_postagem):
    postagem_a_excluir = Postagem.query.filter_by(id_postagem=id_postagem).first()
    if not postagem_a_excluir:
        return jsonify({'mensagem': 'Postagem não encontrada.'})
    
    db.session.delete(postagem_a_excluir)
    db.session.commit()
    
    return jsonify({'mensagem' : 'postagem excluída com sucesso'}, 200)

@app.route('/autores')
# @validar_token
def consultar_autores():
    autores = Autor.query.all()
    lista_de_autores = []
    for autor in autores:
        autor_atual = {}
        autor_atual['id_autor'] = autor.id_autor
        autor_atual['nome'] = autor.nome
        autor_atual['email'] = autor.email
        lista_de_autores.append(autor_atual)

    return jsonify({'autores': lista_de_autores})

@app.route('/autor/<int:id_autor>', methods=['GET'])
# @validar_token
def consultar_autor_por_id(id_autor):
    autor = Autor.query.filter_by(id_autor=id_autor).first()
    if not autor:
        return jsonify('Autor não encontrado.')
    autor_atual = {}
    autor_atual['id_autor'] = autor.id_autor
    autor_atual['nome'] = autor.nome
    autor_atual['email'] = autor.email

    return jsonify({'autor': autor_atual})

@app.route('/autor', methods= ['POST'])
@validar_token
def adicionar_autor(autor):
    novo_autor = request.get_json()
    autor = Autor(nome=novo_autor['nome'], email=novo_autor['email'], senha=novo_autor['senha'])
    
    db.session.add(autor)
    db.session.commit()

    return jsonify(f'Autor: {novo_autor} adicionado com sucesso.', 200)

@app.route('/autor/<int:id_autor>', methods= ['PUT'])
@validar_token
def alterar_informacoes_autor(autor, id_autor):
    autor_a_alterar = request.get_json()
    autor = Autor.query.filter_by(id_autor=id_autor).first()
    try:
        if not autor:
            return jsonify({'mensagem': 'autor não encontrado.'})
    except:
        pass
    
    try:
        autor.nome = autor_a_alterar['nome']
    except:
        pass
    
    try:
        autor.email = autor_a_alterar['email']
    except:
        pass
    
    try:
        autor.senha = autor_a_alterar['senha']
    except:
        pass
    
    db.session.commit()
    
    return jsonify({'Opção atualizada': autor_a_alterar})

@app.route('/autor/<int:id_autor>', methods=['DELETE'])
@validar_token
def apagar_autor(autor, id_autor):
    autor_a_deletar = Autor.query.filter_by(id_autor=id_autor).first()
    if not autor_a_deletar:
        return jsonify({'mensagem': 'autor não encontrado!'})

    db.session.delete(autor_a_deletar)
    db.session.commit()

    return jsonify({'mensagem': 'autor excluído com sucesso'})

# app.run(port=5000,host='localhost',debug=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)