from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

def load_model():
    """Load the sentence transformer model"""
    return SentenceTransformer('all-MiniLM-L6-v2')

def get_embeddings(df, model):
    """Generate embeddings for customer data"""
    features = []
    for _, row in df.iterrows():
        feature_str = f"""
        Purchases: {', '.join(row['Purchase History'])}
        Interests: {', '.join(row['Interests'])}
        Sentiment: {row['Sentiment Score']}
        Engagement: {row['Engagement Score']}
        Age: {row['Age']}
        Gender: {row['Gender']}
        Social: {row['Social Media Activity']}
        """
        features.append(feature_str)
    return model.encode(features)

def get_similarity_matrix(embeddings):
    """Calculate cosine similarity matrix"""
    return cosine_similarity(embeddings)