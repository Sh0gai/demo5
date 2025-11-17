import pymysql
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Connect to the database
try:
    connection = pymysql.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )

    cursor = connection.cursor()

    print("Running migration to add archived columns...")

    # Add archived column to customer table
    try:
        cursor.execute("ALTER TABLE customer ADD COLUMN archived BOOLEAN DEFAULT FALSE")
        print("[OK] Added archived column to customer table")
    except pymysql.err.OperationalError as e:
        if "Duplicate column name" in str(e):
            print("[OK] archived column already exists in customer table")
        else:
            raise

    # Add archived column to pizza table
    try:
        cursor.execute("ALTER TABLE pizza ADD COLUMN archived BOOLEAN DEFAULT FALSE")
        print("[OK] Added archived column to pizza table")
    except pymysql.err.OperationalError as e:
        if "Duplicate column name" in str(e):
            print("[OK] archived column already exists in pizza table")
        else:
            raise

    # Update existing records to not be archived
    cursor.execute("UPDATE customer SET archived = FALSE WHERE archived IS NULL")
    cursor.execute("UPDATE pizza SET archived = FALSE WHERE archived IS NULL")
    print("[OK] Updated existing records")

    # Commit the changes
    connection.commit()
    print("\n[SUCCESS] Migration completed successfully!")

except Exception as e:
    print(f"[ERROR] Error running migration: {e}")
finally:
    if connection:
        cursor.close()
        connection.close()
