# Personal Expense Tracker — ER Diagram

## Entities

### 1. USERS

- **id** — Primary Key
- name
- email — Unique
- password_hash
- is_verified
- verification_token_hash
- verification_expires_at
- created_at

### 2. CATEGORIES

- **category_id** — Primary Key
- category_name — Unique

### 3. EXPENSES

- **expense_id** — Primary Key
- expense_date
- category_id — Foreign Key referencing `CATEGORIES.category_id`
- amount
- description
- payment_method
- user_id — Nullable; a foreign-key constraint referencing `USERS.id` has not been verified

## Relationships

- One category can be associated with many expenses.
- Each expense references a category through `category_id`.
- The `expenses.user_id` column stores a user ID, but a foreign-key constraint linking it to `users.id` has not been verified.

## Mermaid ER Diagram

```mermaid
erDiagram
    CATEGORIES ||--o{ EXPENSES : categorizes

    USERS {
        int id PK
        varchar name
        varchar email UK
        varchar password_hash
        boolean is_verified
        char verification_token_hash
        datetime verification_expires_at
        timestamp created_at
    }

    CATEGORIES {
        int category_id PK
        varchar category_name UK
    }

    EXPENSES {
        int expense_id PK
        date expense_date
        int category_id FK
        decimal amount
        varchar description
        varchar payment_method
        int user_id
    }
```

**Note:** This diagram documents the known schema. The `user_id` column is included in `EXPENSES`, but no relationship between `USERS` and `EXPENSES` is drawn because the corresponding foreign-key constraint has not been verified.
