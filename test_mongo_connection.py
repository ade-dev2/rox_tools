"""Quick MongoDB connection test."""
from pymongo import MongoClient
import toml

# Load secrets from Streamlit secrets
secrets = toml.load(".streamlit/secrets.toml")
mongo_uri = secrets["mongodb"]["uri"]

print(f"Connecting to: rox-cluster.xqzb8pb.mongodb.net")

try:
    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
    # Ping the server
    client.admin.command('ping')
    print("✓ Connection successful!")
    
    # List databases
    dbs = client.list_database_names()
    print(f"✓ Databases: {dbs}")
    
except Exception as e:
    print(f"✗ Connection failed: {e}")
