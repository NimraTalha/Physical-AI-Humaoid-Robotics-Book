"""
Database initialization script for user authentication.
Creates the users table in Neon PostgreSQL.
"""
import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("❌ ERROR: DATABASE_URL not found in .env file")
    print("Please set up Neon PostgreSQL and update backend/.env")
    sys.exit(1)

# SQL schema for the users table
CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    software_background TEXT,
    hardware_background TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index for fast username and email lookups
CREATE INDEX IF NOT EXISTS idx_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_email ON users(email);
"""

def main():
    """Initialize database with users table."""
    print("🔧 Initializing Neon PostgreSQL database for authentication...")
    print(f"📍 Database URL: {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else 'Invalid URL'}")

    try:
        # Connect to database
        conn = psycopg2.connect(DATABASE_URL)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()

        # Execute schema creation
        print("\n📝 Creating users table...")
        cursor.execute(CREATE_TABLE_SQL)

        # Verify table creation
        cursor.execute("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name = 'users'
            ORDER BY ordinal_position;
        """)

        columns = cursor.fetchall()
        if columns:
            print("\n✅ Table 'users' created successfully!")
            print("\n📊 Schema:")
            for col_name, col_type, nullable in columns:
                null_str = "NULL" if nullable == "YES" else "NOT NULL"
                print(f"  - {col_name:20} {col_type:20} {null_str}")
        else:
            print("\n⚠️  Warning: Table 'users' may not have been created")

        # Check indexes
        cursor.execute("""
            SELECT indexname, indexdef
            FROM pg_indexes
            WHERE tablename = 'users';
        """)

        indexes = cursor.fetchall()
        if indexes:
            print("\n🔍 Indexes:")
            for idx_name, idx_def in indexes:
                print(f"  - {idx_name}")

        cursor.close()
        conn.close()

        print("\n✨ Authentication database initialization complete!")

    except psycopg2.OperationalError as e:
        print(f"\n❌ Database connection failed: {e}")
        print("\n💡 Troubleshooting:")
        print("  1. Check DATABASE_URL in backend/.env")
        print("  2. Verify Neon project is active (not paused)")
        print("  3. Check network connectivity")
        sys.exit(1)

    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
