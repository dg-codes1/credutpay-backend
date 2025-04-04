# CREDUTPAY-BACKEND

Projeto desenvolvido para o criar usuários e fazer transações entre suas carteiras

## Descrição

O projeto foi desenolvido para o teste djando e consiste em:

- Autenticação
- Criar um usuário
- Consultar saldo da carteira de um usuário
- Adicionar saldo à carteira
- Criar uma transferência entre usuários (carteiras)
- Listar transferências realizadas por um usuário, com filtro opcional por período de data

## Iniciando

### Dependências

- O projeto foi desenvolvido com [python 3.11](https://www.python.org/downloads/release/python-3110/)

### Antes de começar

* Clone o repositório localmente
* Certifique-se de ter o python instalado
* Certifique-se de ter uma instância de postgres ativa
* Crie ou atualize o arquivo .env com base no .env.example caso não exista

### Executando o programa

* Instale as dependências
```
pip install requirements.txt
```

* Para criar um banco postgres execute
```
docker run -d --name nome -e POSTGRES_USER=meu_usuario -e POSTGRES_PASSWORD=minha_senha -e POSTGRES_DB=nome_do_banco -p 5432:5432 postgres
```

* Execute as migrações do banco
```
python manage.py migrate
```

* Execute a seed para popular o banco de dados se necessário
```
python manage.py seed_users
```

* Os usuários mock criados para teste serão:
- 1 username="seeduser1", password="password1"
- 2 username="seeduser2", password="password2"

* Execute o projeto
```
python manage.py runserver
```

* Execute o projeto com docker
```
docker-compose up --build
```

## Autor

ex. Douglas Claudino Machado  
ex. [douglascmachado](https://www.linkedin.com/in/douglascmachado/)
