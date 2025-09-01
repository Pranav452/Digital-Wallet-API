#!/usr/bin/env python3
"""
Database seeding script for Digital Wallet API
Creates sample users and transactions for testing
"""

from db import SessionLocal, engine
from app.models.User_Management import UserManagement
from app.models.Transaction_Management import TransactionManagement
from datetime import datetime
import uuid

def seed_database():
    db = SessionLocal()
    
    try:
        # Clear existing data
        db.query(TransactionManagement).delete()
        db.query(UserManagement).delete()
        db.commit()
        
        print("Cleared existing data")
        
        # Create sample users
        users = [
            UserManagement(
                username="john_doe",
                email="john@example.com",
                password="password123",
                phone_number="+1234567890"
            ),
            UserManagement(
                username="jane_smith",
                email="jane@example.com",
                password="password456",
                phone_number="+1987654321"
            ),
            UserManagement(
                username="bob_wilson",
                email="bob@example.com",
                password="password789",
                phone_number="+1122334455"
            ),
            UserManagement(
                username="alice_johnson",
                email="alice@example.com",
                password="passwordabc",
                phone_number="+1555666777"
            ),
            UserManagement(
                username="charlie_brown",
                email="charlie@example.com",
                password="passworddef",
                phone_number="+1999888777"
            )
        ]
        
        for user in users:
            db.add(user)
        
        db.commit()
        
        # Refresh users to get their IDs
        for user in users:
            db.refresh(user)
        
        print(f"Created {len(users)} users")
        
        # Create sample transactions
        transactions = []
        
        # Initial wallet loads
        transactions.append(TransactionManagement(
            user_id=users[0].id,
            transaction_type="CREDIT",
            amount=100.00,
            description="Initial wallet load"
        ))
        
        transactions.append(TransactionManagement(
            user_id=users[1].id,
            transaction_type="CREDIT",
            amount=50.00,
            description="Initial wallet load"
        ))
        
        transactions.append(TransactionManagement(
            user_id=users[2].id,
            transaction_type="CREDIT",
            amount=200.00,
            description="Initial wallet load"
        ))
        
        transactions.append(TransactionManagement(
            user_id=users[3].id,
            transaction_type="CREDIT",
            amount=75.00,
            description="Initial wallet load"
        ))
        
        transactions.append(TransactionManagement(
            user_id=users[4].id,
            transaction_type="CREDIT",
            amount=150.00,
            description="Initial wallet load"
        ))
        
        # Add money transactions
        transactions.append(TransactionManagement(
            user_id=users[0].id,
            transaction_type="CREDIT",
            amount=50.00,
            description="Added money to wallet"
        ))
        
        transactions.append(TransactionManagement(
            user_id=users[1].id,
            transaction_type="CREDIT",
            amount=25.00,
            description="Added money to wallet"
        ))
        
        # Withdraw transactions
        transactions.append(TransactionManagement(
            user_id=users[0].id,
            transaction_type="DEBIT",
            amount=25.00,
            description="Withdrew money from wallet"
        ))
        
        transactions.append(TransactionManagement(
            user_id=users[2].id,
            transaction_type="DEBIT",
            amount=50.00,
            description="Withdrew money from wallet"
        ))
        
        # Add all basic transactions first
        for transaction in transactions:
            db.add(transaction)
        
        db.commit()
        
        # Refresh transactions to get their IDs
        for transaction in transactions:
            db.refresh(transaction)
        
        # Transfer transactions
        # Transfer from john to jane
        sender_transaction_1 = TransactionManagement(
            user_id=users[0].id,
            transaction_type="TRANSFER_OUT",
            amount=25.00,
            description="Transfer to jane_smith",
            recipient_user_id=users[1].id
        )
        
        recipient_transaction_1 = TransactionManagement(
            user_id=users[1].id,
            transaction_type="TRANSFER_IN",
            amount=25.00,
            description="Transfer from john_doe",
            reference_transaction_id=None,  # Will be set after flush
            recipient_user_id=users[0].id
        )
        
        db.add(sender_transaction_1)
        db.add(recipient_transaction_1)
        db.flush()
        
        # Link the transactions
        sender_transaction_1.reference_transaction_id = recipient_transaction_1.id
        recipient_transaction_1.reference_transaction_id = sender_transaction_1.id
        
        # Transfer from bob to alice
        sender_transaction_2 = TransactionManagement(
            user_id=users[2].id,
            transaction_type="TRANSFER_OUT",
            amount=30.00,
            description="Transfer to alice_johnson",
            recipient_user_id=users[3].id
        )
        
        recipient_transaction_2 = TransactionManagement(
            user_id=users[3].id,
            transaction_type="TRANSFER_IN",
            amount=30.00,
            description="Transfer from bob_wilson",
            reference_transaction_id=None,  # Will be set after flush
            recipient_user_id=users[2].id
        )
        
        db.add(sender_transaction_2)
        db.add(recipient_transaction_2)
        db.flush()
        
        # Link the transactions
        sender_transaction_2.reference_transaction_id = recipient_transaction_2.id
        recipient_transaction_2.reference_transaction_id = sender_transaction_2.id
        
        # Add transfer transactions to the list for counting
        transactions.extend([
            sender_transaction_1, recipient_transaction_1,
            sender_transaction_2, recipient_transaction_2
        ])
        
        # Update user balances based on transactions
        for transaction in transactions:
            user = db.query(UserManagement).filter(UserManagement.id == transaction.user_id).first()
            if user:
                if transaction.transaction_type == "CREDIT":
                    user.balance += transaction.amount
                elif transaction.transaction_type == "DEBIT":
                    user.balance -= transaction.amount
                elif transaction.transaction_type == "TRANSFER_OUT":
                    user.balance -= transaction.amount
                elif transaction.transaction_type == "TRANSFER_IN":
                    user.balance += transaction.amount
                
                user.updated_at = datetime.now()
        
        db.commit()
        
        print(f"Created {len(transactions)} transactions")
        print("Database seeded successfully!")
        
        # Print final balances
        print("\nFinal user balances:")
        for user in users:
            db.refresh(user)
            print(f"{user.username}: ${user.balance:.2f}")
            
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
