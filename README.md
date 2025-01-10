
## 📋 **Descrição**
Esta é uma API desenvolvida com Flask para gerenciamento de **Autores** e **Postagens**.  
A API utiliza autenticação JWT para proteger alguns endpoints, garantindo segurança no acesso aos dados. 

---

## 🚀 **Como Executar o Projeto**

### **Pré-requisitos**  
- Python 3.8 ou superior  
- Banco de Dados configurado (com tabelas `Autor` e `Postagem`)  
- Bibliotecas necessárias (instale com o comando abaixo):  
```bash
pip install flask flask-sqlalchemy flask-jwt-extended
```

### **Execução**
1. Clone o repositório:  
   ```bash
   git clone https://github.com/seu-repositorio/api-flask-autores-postagens.git
   cd api-flask-autores-postagens
   ```
2. Execute o arquivo principal:  
   ```bash
   python app.py
   ```
3. Acesse a API em:  
   ```
   http://localhost:10000
   ```

---

## 🛠️ **Endpoints da API**

### 🔐 **Autenticação**
| Método  | Endpoint  | Descrição |
|---------|-----------|-----------|
| `POST`  | `/login`  | Gera um token JWT ao autenticar com `username` e `password`. |

> **Nota:** Use o token JWT no cabeçalho `x-access-token` para acessar endpoints protegidos.

---

### 📝 **Postagens**
| Método  | Endpoint                       | Descrição                          | Protegido? |
|---------|--------------------------------|------------------------------------|------------|
| `GET`   | `/postagens`                   | Retorna todas as postagens.        | ❌ Não     |
| `GET`   | `/postagem/<id_postagem>`      | Retorna uma postagem pelo ID.      | ❌ Não     |
| `POST`  | `/postagem`                    | Adiciona uma nova postagem.        | ✅ Sim     |
| `PUT`   | `/postagem/<id_postagem>`      | Atualiza uma postagem existente.   | ✅ Sim     |
| `DELETE`| `/postagem/<id_postagem>`      | Exclui uma postagem.               | ✅ Sim     |

---

### 👤 **Autores**
| Método  | Endpoint                  | Descrição                           | Protegido? |
|---------|---------------------------|-------------------------------------|------------|
| `GET`   | `/autores`                | Retorna todos os autores.           | ❌ Não     |
| `GET`   | `/autor/<id_autor>`       | Retorna um autor pelo ID.           | ❌ Não     |
| `POST`  | `/autor`                  | Adiciona um novo autor.             | ✅ Sim     |
| `PUT`   | `/autor/<id_autor>`       | Atualiza informações de um autor.   | ✅ Sim     |
| `DELETE`| `/autor/<id_autor>`       | Exclui um autor.                    | ✅ Sim     |

---

## 🔑 **Autenticação JWT**
1. Autentique-se no endpoint `/login` fornecendo `username` e `password`.  
2. Um token JWT será gerado com validade de 30 minutos.  
3. Utilize o token nos endpoints protegidos no cabeçalho HTTP:  
   ```http
   x-access-token: SEU_TOKEN_JWT
   ```

---

## 📦 **Modelo de Dados**

### **Autor**
```json
{
  "id_autor": 1,
  "nome": "João Silva",
  "email": "joao@email.com",
  "senha": "1234"
}
```

### **Postagem**
```json
{
  "id_postagem": 1,
  "titulo": "Minha Primeira Postagem",
  "id_autor": 1
}
```

---

## 🛡️ **Melhorias Futuras**
- 🔒 **Hash de Senhas**: Usar bcrypt para maior segurança.  
- 🛠️ **Validações**: Garantir entradas mais robustas e seguras.  
- 📖 **Documentação Interativa**: Adicionar suporte ao Swagger ou Postman.  

---
