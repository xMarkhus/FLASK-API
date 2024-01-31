from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os 

load_dotenv()
# criar um API flask
app = Flask(__name__)
# criar uma instância de SQLAlchemy
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')

db = SQLAlchemy(app)
db: SQLAlchemy

# definir a estrutura da tabela postagem
# id_postagem, titulo, autor
class Postagem(db.Model):
    __tablename__ = 'postagem'
    id_postagem = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String)
    id_autor = db.Column(db.Integer, db.ForeignKey('autor.id_autor'))

# definir a estrutura da tabela autor
# id_autor, nome, email, senha, admin, postagens
class Autor(db.Model):
    __tablename__ = 'autor'
    id_autor = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String)
    email = db.Column(db.String)
    senha = db.Column(db.String)
    admin = db.Column(db.Boolean)
    postagens = db.relationship('Postagem')

# criar o banco de dados
def inicializar_banco():
    with app.app_context():
        db.drop_all()
        db.create_all()
        # criar usuários administradores
        autor = Autor(nome=os.getenv('nome'), email=os.getenv('email'), senha = os.getenv('senha'), admin = True)
        db.session.add(autor)
        db.session.commit()

if __name__ == '__main__':
    inicializar_banco()
