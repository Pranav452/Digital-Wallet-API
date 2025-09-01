# Digital Wallet API

A FastAPI backend application that functions as a digital wallet system, allowing users to manage their wallets, maintain transaction records, and simulate money transfers between users.

## Features

- **User Management**: Create, retrieve, and update user profiles
- **Wallet Operations**: Check balance, add money, and withdraw money
- **Transaction Management**: Record and retrieve transaction history with pagination
- **Transfer System**: Peer-to-peer money transfers with atomic operations
- **Database**: SQLite database with proper relationships and constraints

## API Endpoints

### User Management
- `POST /users` - Create a new user
- `GET /users/{user_id}` - Get user profile
- `PUT /users/{user_id}` - Update user profile

### Wallet Operations
- `GET /wallet/{user_id}/balance` - Get wallet balance
- `POST /wallet/{user_id}/add-money` - Add money to wallet
- `POST /wallet/{user_id}/withdraw` - Withdraw money from wallet

### Transaction Management
- `GET /transactions/{user_id}` - Get user's transaction history (paginated)
- `GET /transactions/detail/{transaction_id}` - Get transaction details
- `POST /transactions` - Create a new transaction

### Transfer System
- `POST /transfer` - Transfer money between users
- `GET /transfer/{transfer_id}` - Get transfer details

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    phone_number VARCHAR(15),
    balance DECIMAL(10,2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Transactions Table
```sql
CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    transaction_type VARCHAR(20) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    description TEXT,
    reference_transaction_id INTEGER REFERENCES transactions(id),
    recipient_user_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Setup Instructions

### Prerequisites
- Python 3.9 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Digital-Wallet-API
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

   The API will be available at `http://localhost:8000`

5. **Seed the database with sample data (optional)**
   ```bash
   python seed_data.py
   ```

## API Documentation

Once the application is running, you can access:
- **Interactive API docs**: `http://localhost:8000/docs` (Swagger UI)
- **Alternative API docs**: `http://localhost:8000/redoc` (ReDoc)

## Sample Data

The seeding script creates 5 sample users with various transactions:
- **john_doe**: $125.00 (after initial load, add money, withdraw, and transfer)
- **jane_smith**: $75.00 (after initial load, add money, and receiving transfer)
- **bob_wilson**: $120.00 (after initial load, withdraw, and transfer)
- **alice_johnson**: $105.00 (after initial load and receiving transfer)
- **charlie_brown**: $150.00 (initial load only)

## Business Logic Features

- **Balance Management**: Automatic balance calculation and updates
- **Transaction Integrity**: All transactions are timestamped and linked appropriately
- **Atomic Transfers**: Transfer operations are atomic - both succeed or both fail
- **Data Validation**: Positive amounts, proper decimal places, and user validation
- **Error Handling**: Comprehensive error handling with appropriate HTTP status codes

## Testing the API

### Create a User
```bash
curl -X POST "http://localhost:8000/users" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "test_user",
       "email": "test@example.com",
       "password": "password123",
       "phone_number": "+1234567890"
     }'
```

### Check Wallet Balance
```bash
curl "http://localhost:8000/wallet/1/balance"
```

### Add Money to Wallet
```bash
curl -X POST "http://localhost:8000/wallet/1/add-money" \
     -H "Content-Type: application/json" \
     -d '{
       "amount": 50.00,
       "description": "Test deposit"
     }'
```

### Transfer Money
```bash
curl -X POST "http://localhost:8000/transfer" \
     -H "Content-Type: application/json" \
     -d '{
       "sender_user_id": 1,
       "recipient_user_id": 2,
       "amount": 25.00,
       "description": "Test transfer"
     }'
```

## Project Structure

```
Digital-Wallet-API/
├── app/
│   ├── crud/           # Database operations
│   ├── models/         # SQLAlchemy models
│   ├── routers/        # API route definitions
│   └── schema/         # Pydantic models
├── main.py             # FastAPI application entry point
├── db.py               # Database configuration
├── seed_data.py        # Database seeding script
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Development

### Running Tests
```bash
pytest
```

### Database Migrations
The application uses SQLAlchemy with automatic table creation. For production use, consider using Alembic for database migrations.

### Code Style
The code follows PEP 8 guidelines and uses type hints throughout.

## Security Notes

- Passwords are stored as plain text in this demo - in production, use proper hashing (e.g., bcrypt)
- Consider implementing authentication and authorization
- Validate and sanitize all user inputs
- Use HTTPS in production

## License

This project is created for educational purposes as part of the Masai School curriculum.
