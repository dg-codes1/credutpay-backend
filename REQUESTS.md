### Documentação das Rotas da API

#### **Autenticação**
- **POST `/api/token`**  
  Gera um token de acesso e refresh para autenticação.  
  **Body**:  
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
  **Response**:  
  ```json
  {
    "refresh": "string",
    "access": "string"
  }
  ```

- **POST `/api/token/refresh`**  
  Atualiza o token de acesso usando o token de refresh.  
  **Body**:  
  ```json
  {
    "refresh": "string"
  }
  ```
  **Response**:  
  ```json
  {
    "access": "string"
  }
  ```

#### **Usuários**
- **POST `/api/users/create`**  
  Cria um novo usuário.  
  **Body**:  
  ```json
  {
    "username": "string",
    "email": "string",
    "password": "string"
  }
  ```
  **Response**:  
  ```json
  {
    "uuid": "string",
    "username": "string",
    "email": "string",
    "wallet_balance": "number"
  }
  ```

- **GET `/api/users/{id}/get_balance`**  
  Retorna o saldo da carteira do usuário autenticado.  
  **Response**:  
  ```json
  {
    "balance": "number"
  }
  ```

- **POST `/api/users/{id}/add_balance`**  
  Adiciona saldo à carteira do usuário autenticado.  
  **Body**:  
  ```json
  {
    "value": "number"
  }
  ```
  **Response**:  
  ```json
  {
    "wallet_balance": "number"
  }
  ```

#### **Transferências**
- **POST `/api/transfers`**  
  Cria uma transferência entre usuários.  
  **Body**:  
  ```json
  {
    "payer": "uuid",
    "receiver": "uuid",
    "value": "number"
  }
  ```
  **Response**:  
  ```json
  {
    "message": "Transfer was successful"
  }
  ```

- **GET `/api/transfers`**  
  Lista as transferências realizadas pelo usuário autenticado.  
  **Query Params**:  
  - `from_date` (opcional): Data inicial no formato `YYYY-MM-DD`.  
  - `to_date` (opcional): Data final no formato `YYYY-MM-DD`.  
  **Response**:  
  ```json
  [
    {
      "uuid": "string",
      "payer_username": "string",
      "receiver_username": "string",
      "value": "number",
      "date_time": "string"
    }
  ]
  ```