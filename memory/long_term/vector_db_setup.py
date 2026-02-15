import chromadb

def setup_vector_db():
    """
    Initializes the ChromaDB client and creates a collection for the swarm.
    """
    try:
        # Using an in-memory instance of ChromaDB for simplicity.
        # For production, you would use a persistent client:
        # client = chromadb.PersistentClient(path="/path/to/db")
        client = chromadb.Client()

        # Create a collection to store agent memories.
        # The 'get_or_create_collection' method is idempotent.
        collection = client.get_or_create_collection(name="titanforge_memory")

        print("ChromaDB client initialized and 'titanforge_memory' collection is ready.")
        return collection
    except Exception as e:
        print(f"Error setting up ChromaDB: {e}")
        return None

if __name__ == "__main__":
    setup_vector_db()
