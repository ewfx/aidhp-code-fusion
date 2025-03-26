# Import required libraries
import numpy as np
import plotly.express as px
from datetime import datetime
import random
import requests  # New import for API calls

# Generate product recommendations for existing customers
def recommend_products(customer_data, df, similarity_matrix, strategy="hybrid", api_key=None):
    if api_key:
        # API-based recommendation logic
        try:
            # Prepare payload for API request
            payload = {
                "customer_data": customer_data,
                "strategy": strategy,
                "similarity_data": similarity_matrix[idx].tolist() if 'idx' in locals() else []
            }
            headers = {"Authorization": f"Bearer {api_key}"}
            response = requests.post(
                "https://api.recommendation-engine.com/recommend",  # Hypothetical API endpoint
                json=payload,
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            api_recs = response.json().get("recommendations", [])
            return api_recs  # Assuming API returns in compatible format
        except Exception as e:
            print(f"API request failed: {e}")
            # Fallback to simulated responses if API fails

    # Existing simulated response logic
    idx = df.index[df["Customer Name"] == customer_data["Customer Name"]].tolist()[0]
    
    # Get similar users using collaborative filtering
    similar_users = np.argsort(similarity_matrix[idx])[-3:][::-1]
    similar_users = [u for u in similar_users if u != idx]
    
    # Collect recommendations from similar users
    collab_recs = set()
    for user in similar_users:
        collab_recs.update(df.iloc[user]["Purchase History"])
    
    # Filter out items customer already has
    existing_items = set(customer_data["Purchase History"])
    collab_recs = list(collab_recs - existing_items)
    
    # Filter recommendations based on customer interests
    filtered_collab_recs = []
    for rec in collab_recs:
        if any(interest.lower() in rec.lower() for interest in customer_data["Interests"]):
            filtered_collab_recs.append(rec)
    
    # Use unfiltered recommendations if no matches found
    if not filtered_collab_recs:
        filtered_collab_recs = collab_recs
    
    # Map of interests to potential products
    interest_map = {
        "Tech": ["Wireless Keyboard", "External SSD"],
        "Gaming": ["Gaming Mouse", "Mechanical Keyboard"],
        "Fashion": ["Designer Watch", "Silk Scarf"],
        "Winter Wear": ["Winter Boots", "Wool Gloves"],
        "Mobile": ["Phone Stand", "Screen Protector"],
        "Accessories": ["Smart Watch", "Wireless Earbuds"],
        "Photography": ["Camera Bag", "Lens Cleaner"],
        "Gadgets": ["Smart Speaker", "Fitness Tracker"],
        "Luxury": ["Premium Credit Card", "Investment Portfolio"],
        "Travel": ["Travel Insurance", "Currency Exchange Card"]
    }
    
    # Generate contextual recommendations based on interests
    context_recs = []
    for interest in customer_data["Interests"]:
        if interest in interest_map:
            context_recs.extend(interest_map[interest])
    
    # Assess customer risk score
    risk_score = assess_risk(customer_data)
    
    # Combine recommendations based on selected strategy
    if strategy == "collaborative":
        all_recs = filtered_collab_recs
    elif strategy == "contextual":
        all_recs = context_recs
    else:  # hybrid
        all_recs = list(set(filtered_collab_recs + context_recs))
    
    # Score and sort recommendations
    final_recs = []
    for rec in all_recs:
        rec_score = score_recommendation(rec, customer_data, risk_score, strategy)
        final_recs.append({"product": rec, "score": rec_score, "reason": get_reason(rec, customer_data), "risk": risk_score})
    
    return sorted(final_recs, key=lambda x: x["score"], reverse=True)[:5]

# Generate recommendations for new customers based on interests
def recommend_new_customer(customer_data, api_key=None):
    if api_key:
        # API-based recommendation logic
        try:
            payload = {"customer_data": customer_data}
            headers = {"Authorization": f"Bearer {api_key}"}
            response = requests.post(
                "https://api.recommendation-engine.com/recommend-new",  # Hypothetical API endpoint
                json=payload,
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            api_recs = response.json().get("recommendations", [])
            return api_recs  # Assuming API returns in compatible format
        except Exception as e:
            print(f"API request failed: {e}")
            # Fallback to simulated responses if API fails

    # Existing simulated response logic
    # Map of interests to potential products
    interest_map = {
        "Tech": ["Wireless Keyboard", "External SSD"],
        "Gaming": ["Gaming Mouse", "Mechanical Keyboard"],
        "Fashion": ["Designer Watch", "Silk Scarf"],
        "Winter Wear": ["Winter Boots", "Wool Gloves"],
        "Mobile": ["Phone Stand", "Screen Protector"],
        "Accessories": ["Smart Watch", "Wireless Earbuds"],
        "Photography": ["Camera Bag", "Lens Cleaner"],
        "Gadgets": ["Smart Speaker", "Fitness Tracker"],
        "Luxury": ["Premium Credit Card", "Investment Portfolio"],
        "Travel": ["Travel Insurance", "Currency Exchange Card"]
    }
    
    # Generate recommendations based on interests
    context_recs = []
    for interest in customer_data["Interests"]:
        if interest in interest_map:
            context_recs.extend(interest_map[interest])
    
    # Assess customer risk score
    risk_score = assess_risk(customer_data)
    
    # Score and sort recommendations
    final_recs = []
    for rec in context_recs:
        rec_score = score_recommendation(rec, customer_data, risk_score, "contextual")
        final_recs.append({"product": rec, "score": rec_score, "reason": get_reason(rec, customer_data), "risk": risk_score})
    
    return sorted(final_recs, key=lambda x: x["score"], reverse=True)[:5]

# Calculate basic risk score based on sentiment and engagement
def assess_risk(customer_data):
    risk = 0
    if customer_data["Sentiment Score"] < -0.5:
        risk += 0.3
    if customer_data["Engagement Score"] < 30:
        risk += 0.2
    return min(risk, 1.0)

# Score recommendations based on multiple factors
def score_recommendation(product, customer_data, risk_score, strategy):
    base_score = 0.5
    
    # Adjust score based on interest match
    interest_match = any(interest.lower() in product.lower() for interest in customer_data["Interests"])
    if interest_match:
        base_score += 0.3
        if strategy == "contextual":
            base_score += 0.2
    else:
        base_score -= 0.2
    
    # Adjust score based on purchase history alignment
    purchase_categories = set()
    for purchase in customer_data["Purchase History"]:
        for interest, products in {
            "Tech": ["Laptop", "Mouse", "Wireless Keyboard", "External SSD"],
            "Gaming": ["Gaming Mouse", "Mechanical Keyboard"],
            "Fashion": ["Shoes", "Jacket", "Designer Watch", "Silk Scarf"],
            "Winter Wear": ["Winter Boots", "Wool Gloves"],
            "Mobile": ["Phone", "Phone Stand", "Screen Protector"],
            "Accessories": ["Earbuds", "Smart Watch", "Wireless Earbuds"],
            "Photography": ["Camera", "Tripod", "Camera Bag", "Lens Cleaner"],
            "Gadgets": ["Smart Speaker", "Fitness Tracker"],
            "Luxury": ["Watch", "Sunglasses", "Premium Credit Card", "Investment Portfolio"],
            "Travel": ["Travel Insurance", "Currency Exchange Card"]
        }.items():
            if purchase in products:
                purchase_categories.add(interest)
    if any(category.lower() in product.lower() for category in purchase_categories):
        base_score += 0.15
        if strategy == "collaborative":
            base_score += 0.2
    
    # Adjust score for insurance products if risk is high
    if risk_score > 0.5 and "Insurance" in product:
        base_score += 0.2
    
    # Adjust score based on engagement level
    if customer_data["Engagement Score"] > 80:
        base_score += 0.1
    
    # Adjust score based on sentiment
    if customer_data["Sentiment Score"] > 0:
        base_score += 0.05 * customer_data["Sentiment Score"]
    
    return min(max(base_score, 0.0), 1.0)

# Generate human-readable reasons for recommendations
def get_reason(product, customer_data):
    reasons = []
    
    # Add interest-based reason if applicable
    matching_interests = [interest for interest in customer_data["Interests"] if interest.lower() in product.lower()]
    if matching_interests:
        interest_phrases = [
            f"Perfect for your passion in {', '.join(matching_interests)}!",
            f"Designed for {', '.join(matching_interests)} lovers like you!",
            f"Enhance your {', '.join(matching_interests)} experience with this!"
        ]
        reasons.append(random.choice(interest_phrases))
    
    # Add purchase history reason if applicable
    purchase_categories = set()
    for purchase in customer_data["Purchase History"]:
        for interest, products in {
            "Tech": ["Laptop", "Mouse", "Wireless Keyboard", "External SSD"],
            "Gaming": ["Gaming Mouse", "Mechanical Keyboard"],
            "Fashion": ["Shoes", "Jacket", "Designer Watch", "Silk Scarf"],
            "Winter Wear": ["Winter Boots", "Wool Gloves"],
            "Mobile": ["Phone", "Phone Stand", "Screen Protector"],
            "Accessories": ["Earbuds", "Smart Watch", "Wireless Earbuds"],
            "Photography": ["Camera", "Tripod", "Camera Bag", "Lens Cleaner"],
            "Gadgets": ["Smart Speaker", "Fitness Tracker"],
            "Luxury": ["Watch", "Sunglasses", "Premium Credit Card", "Investment Portfolio"],
            "Travel": ["Travel Insurance", "Currency Exchange Card"]
        }.items():
            if purchase in products:
                purchase_categories.add(interest)
    if any(category.lower() in product.lower() for category in purchase_categories):
        purchase_phrases = [
            f"Pairs well with your {', '.join(customer_data['Purchase History'])}!",
            f"Complements your recent purchase of {', '.join(customer_data['Purchase History'])}!",
            f"A great addition to your {', '.join(customer_data['Purchase History'])} setup!"
        ]
        reasons.append(random.choice(purchase_phrases))
    
    # Add product-specific reasons if available
    product_phrases = {
        "Gaming Mouse": ["Level up your gaming with precision control!"],
        "Mechanical Keyboard": ["Experience the ultimate typing and gaming performance!"],
        "Wireless Keyboard": ["Boost your productivity with seamless connectivity!"],
        "External SSD": ["Store your tech projects with lightning-fast speed!"],
        "Phone": ["Stay connected with the latest smartphone technology!"],
        "Phone Stand": ["Keep your device handy while you work or play!"],
        "Screen Protector": ["Protect your phone in style!"],
        "Earbuds": ["Immerse yourself in music on the go!"],
        "Smart Watch": ["Track your fitness and stay connected!"],
        "Wireless Earbuds": ["Enjoy wireless freedom with crystal-clear sound!"],
        "Camera": ["Capture every moment with stunning clarity!"],
        "Camera Bag": ["Keep your photography gear safe and organized!"],
        "Lens Cleaner": ["Ensure your shots are always crystal clear!"],
        "Smart Speaker": ["Bring your home to life with smart audio!"],
        "Fitness Tracker": ["Stay motivated with your fitness goals!"],
        "Designer Watch": ["Add a touch of elegance to your style!"],
        "Silk Scarf": ["Elevate your fashion with this luxurious accessory!"],
        "Winter Boots": ["Stay warm and stylish this winter!"],
        "Wool Gloves": ["Keep your hands cozy in the cold!"],
        "Premium Credit Card": ["Unlock exclusive benefits with this card!"],
        "Investment Portfolio": ["Secure your financial future with smart investments!"],
        "Travel Insurance": ["Travel with peace of mind!"],
        "Currency Exchange Card": ["Make international travel hassle-free!"]
    }
    if product in product_phrases:
        reasons.append(random.choice(product_phrases[product]))
    
    # Add sentiment-based reason if applicable
    if customer_data["Sentiment Score"] > 0.5:
        sentiment_phrases = [
            "You seem to be in a great mood—treat yourself with this!",
            "Celebrate your positive vibes with this awesome product!",
            "Your happiness deserves this special addition!"
        ]
        reasons.append(random.choice(sentiment_phrases))
    elif customer_data["Sentiment Score"] < -0.5:
        sentiment_phrases = [
            "This might help lift your spirits!",
            "Brighten your day with this fantastic product!",
            "A little something to cheer you up!"
        ]
        reasons.append(random.choice(sentiment_phrases))
    
    # Add engagement-based reason if applicable
    if customer_data["Engagement Score"] > 80:
        engagement_phrases = [
            "As one of our most engaged users, we think you'll love this!",
            "Your active engagement makes this a perfect fit for you!",
            "We picked this just for a loyal user like you!"
        ]
        reasons.append(random.choice(engagement_phrases))
    
    # Add risk-based reason if applicable
    risk_score = assess_risk(customer_data)
    if risk_score > 0.5 and "Insurance" in product:
        risk_phrases = [
            "A smart choice to secure your future!",
            "Protect what matters most with this!",
            "Ensure peace of mind with this essential product!"
        ]
        reasons.append(random.choice(risk_phrases))
    
    # Add age-based reason if applicable
    if customer_data["Age"] < 30:
        age_phrases = [
            "A trendy pick for young enthusiasts like you!",
            "Young and tech-savvy? This is for you!",
            "Perfect for the next generation of innovators!"
        ]
        reasons.append(random.choice(age_phrases))
    elif customer_data["Age"] > 50:
        age_phrases = [
            "A reliable choice tailored for your needs!",
            "Designed with your experience in mind!",
            "A timeless addition for seasoned users!"
        ]
        reasons.append(random.choice(age_phrases))
    
    # Add social media activity reason if applicable
    if customer_data["Social Media Activity"] == "High":
        social_phrases = [
            "Share your experience with this on social media!",
            "Show off this awesome product to your followers!",
            "This is worth posting about on your socials!"
        ]
        reasons.append(random.choice(social_phrases))
    
    # Add fallback reason if no other reasons apply
    if not reasons:
        fallback_phrases = [
            "A great addition to your collection!",
            "We think you'll enjoy this product!",
            "A fantastic choice for someone like you!"
        ]
        reasons.append(random.choice(fallback_phrases))
    
    # Return 1-2 reasons for brevity
    return " ".join(random.sample(reasons, min(len(reasons), 2)))

# Create radar chart visualization of customer profile
def plot_customer_insights(customer_data):
    categories = ['Sentiment', 'Engagement', 'Social Activity', 'Risk']
    
    # Calculate values for each metric
    sentiment_value = max(0, customer_data['Sentiment Score'] + 1)
    engagement_value = customer_data['Engagement Score'] / 100 * 2
    social_activity_value = {"Low": 0, "Medium": 1, "High": 2}[customer_data['Social Media Activity']]
    risk_value = assess_risk(customer_data) * 2
    
    values = [sentiment_value, engagement_value, social_activity_value, risk_value]
    
    # Create hover text for tooltips
    hover_text = [
        f"Sentiment: {sentiment_value:.2f} (Score: {customer_data['Sentiment Score']})",
        f"Engagement: {engagement_value:.2f} (Score: {customer_data['Engagement Score']}/100)",
        f"Social Activity: {social_activity_value:.2f} (Level: {customer_data['Social Media Activity']})",
        f"Risk: {risk_value:.2f} (Score: {assess_risk(customer_data):.2f})"
    ]
    
    # Create radar chart
    fig = px.line_polar(
        r=values + values[:1],
        theta=categories + categories[:1],
        line_close=True,
        title=f"Customer {customer_data['Customer Name']} Profile (Updated: {datetime.now().strftime('%Y-%m-%d')})"
    )
    
    # Customize chart appearance
    fig.update_traces(
        fill='toself',
        fillcolor='rgba(50, 115, 220, 0.5)',
        line_color='rgb(50, 115, 220)',
        hoverinfo='text',
        text=hover_text + hover_text[:1]
    )
    
    # Customize chart layout
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 2],
                tickvals=[0, 0.5, 1, 1.5, 2],
                ticktext=['0', '0.5', '1', '1.5', '2'],
                showline=True,
                gridcolor='lightgray'
            ),
            angularaxis=dict(
                rotation=90,
                direction="clockwise",
                showline=True,
                gridcolor='lightgray',
                tickfont=dict(size=14, color='black')
            )
        ),
        showlegend=False,
        title=dict(
            text=f"Customer {customer_data['Customer Name']} Profile (Updated: {datetime.now().strftime('%Y-%m-%d')})",
            x=0.5,
            xanchor='center',
            font=dict(size=16)
        ),
        margin=dict(l=50, r=50, t=80, b=50),
        height=400,
        width=400
    )
    
    return fig