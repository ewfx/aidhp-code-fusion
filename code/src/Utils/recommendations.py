import numpy as np
import plotly.express as px
import json

def recommend_products(customer_id, df, similarity_matrix, strategy="hybrid"):
    """Generate product recommendations"""
    idx = df.index[df["Customer ID"] == customer_id].tolist()[0]
    customer_data = df.iloc[idx]
    
    # Collaborative filtering
    similar_users = np.argsort(similarity_matrix[idx])[-3:][::-1]
    similar_users = [u for u in similar_users if u != idx]
    
    collab_recs = set()
    for user in similar_users:
        collab_recs.update(df.iloc[user]["Purchase History"])
    
    existing_items = set(customer_data["Purchase History"])
    collab_recs = list(collab_recs - existing_items)
    
    # Contextual recommendations
    interest_map = {
        "Tech": ["Wireless Keyboard", "External SSD"],
        "Gaming": ["Gaming Mouse", "Mechanical Keyboard"],
        "Fashion": ["Designer Watch", "Silk Scarf"],
        "Winter Wear": ["Winter Boots", "Wool Gloves"],
        "Mobile": ["Phone Stand", "Screen Protector"],
        "Accessories": ["Smart Watch", "Wireless Earbuds"],
        "Photography": ["Camera Bag", "Lens Cleaner"],
        "Gadgets": ["Smart Speaker", "Fitness Tracker"],
        "Luxury": ["Leather Wallet", "Premium Sunglasses"],
        "Travel": ["Travel Adapter", "Neck Pillow"]
    }
    
    context_recs = []
    for interest in customer_data["Interests"]:
        if interest in interest_map:
            context_recs.extend(interest_map[interest])
    
    # Hybrid approach
    if strategy == "collaborative":
        return collab_recs[:3]
    elif strategy == "contextual":
        return list(set(context_recs))[:3]
    else:
        return list(set(collab_recs + context_recs))[:5]

def plot_customer_insights(customer_data):
    """Generate customer insights visualization"""
    categories = ['Sentiment', 'Engagement', 'Social Activity']
    values = [
        max(0, customer_data['Sentiment Score'] + 1),
        customer_data['Engagement Score'] / 100 * 2,
        {"Low": 0, "Medium": 1, "High": 2}[customer_data['Social Media Activity']]
    ]
    
    fig = px.line_polar(
        r=values + values[:1],
        theta=categories + categories[:1],
        line_close=True,
        title="Customer Profile Radar Chart"
    )
    fig.update_traces(fill='toself')
    return fig

def get_simulated_response(customer_id):
    """Fallback simulated responses"""
    simulated = {
        101: {
            "products": [
                {"name": "Mechanical Keyboard", "reason": "Enhances gaming setup"},
                {"name": "Gaming Headset", "reason": "Completes tech enthusiast setup"},
                {"name": "USB Hub", "reason": "Useful for multiple devices"}
            ],
            "insights": [
                "High potential for tech accessory bundles",
                "Likely to respond to gaming-related promotions"
            ],
            "messages": [
                "Tech enthusiast? Upgrade your setup with our premium accessories!",
                "Gamer special: 15% off all gaming gear this week!"
            ]
        },
        # ... (other customer responses from original code)
    }
    return simulated.get(customer_id, {"products": [], "insights": [], "messages": []})

def init_openai_client():
    """Initialize OpenAI client with fallback"""
    try:
        import os
        from openai import OpenAI
        
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            return None
            
        client = OpenAI(api_key=api_key)
        return client
    except Exception:
        return None