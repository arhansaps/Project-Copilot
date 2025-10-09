from pinecone import Pinecone, ServerlessSpec
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Pinecone
pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))

index_name = "oee-semantic"

# Check if index exists and create if not
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1536,  # For OpenAI text-embedding-ada-002 or similar
        metric='cosine',
        spec=ServerlessSpec(
            cloud='aws',
            region='us-east-1'
        )
    )
    print(f"✓ Index '{index_name}' created successfully on AWS us-east-1")
else:
    print(f"✓ Index '{index_name}' already exists")

# Connect to the index
index = pc.Index(index_name)

# Get index stats
stats = index.describe_index_stats()
print(f"Index stats: {stats}")