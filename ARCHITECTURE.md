# Documentação de Arquitetura

## **Visão Geral**
A aplicação é uma API para gerenciar usuários e transferências financeiras

---

## **Modelos de dados**

### **User**
Representa os usuários do sistema.

**Campos**:
- `id` (UUID): Identificador único do usuário.
- `username` (String): Nome de usuário.
- `email` (String): Endereço de e-mail.
- `password` (String): Senha do usuário (armazenada de forma segura).
- `wallet_balance` (Decimal): Saldo da carteira do usuário.

**Relacionamentos**:
- Nenhum relacionamento direto com outros modelos.

---

### **Transfer**
Representa uma transferência financeira entre dois usuários.

**Campos**:
- `id` (UUID): Identificador único da transferência.
- `payer` (ForeignKey para `User`): Usuário que realizou o pagamento.
- `receiver` (ForeignKey para `User`): Usuário que recebeu o pagamento.
- `value` (Decimal): Valor da transferência.
- `date_time` (DateTime): Data e hora da transferência.

**Relacionamentos**:
- Relaciona-se com o modelo `User` através de `payer` e `receiver`.

---

## **Fluxo de Dados**

1. **Autenticação**:
   - O usuário realiza login utilizando a rota `/api/token`.
   - Um token JWT é gerado para autenticação nas demais rotas.

2. **Gerenciamento de Usuários**:
   - Um novo usuário pode ser criado através da rota `/api/users/create`.
   - O saldo da carteira pode ser consultado ou atualizado utilizando as rotas `/api/users/{id}/get_balance` e `/api/users/{id}/add_balance`.

3. **Transferências**:
   - Transferências financeiras entre usuários são criadas através da rota `/api/transfers`.
   - O histórico de transferências pode ser consultado utilizando a rota `/api/transfers`.

---

## **Tecnologias Utilizadas**
- **Django**: Framework principal para desenvolvimento web.
- **Django Rest Framework (DRF)**: Extensão para criação de APIs RESTful.
- **SQLite/PostgreSQL**: Banco de dados para persistência de dados.
- **JWT (JSON Web Tokens)**: Utilizado para autenticação e autorização.

---

## **Próximos passos**
- Identificar possíveis colunas e adições nas funcionalidades do usuário na visão de produto
- Implementar swagger para documentação
- Middleware para invalidar refresh tokens para evitar ataques de força bruta
- Uso de Validators

---
