# Import required libraries
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load pre-trained transformer model with caching
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

# Generate embeddings from customer data using the model
def get_embeddings(df, model):
    features = []
    # Create feature strings for each customer
    for _, row in df.iterrows():
        feature_str = f"Purchases: {', '.join(row['Purchase History'])}\nInterests: {', '.join(row['Interests'])}\nSentiment: {row['Sentiment Score']}\nEngagement: {row['Engagement Score']}\nAge: {row['Age']}\nGender: {row['Gender']}\nSocial: {row['Social Media Activity']}"
        features.append(feature_str)
    return model.encode(features)

# Calculate cosine similarity matrix and normalize it
def get_similarity_matrix(embeddings):
    sim_matrix = cosine_similarity(embeddings)
    sim_matrix = (sim_matrix - sim_matrix.min()) / (sim_matrix.max() - sim_matrix.min())
    return sim_matrix