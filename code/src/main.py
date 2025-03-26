import streamlit as st
import pandas as pd
from Utils.data_processing import load_data, preprocess_data
from Utils.embeddings import load_model, get_embeddings, get_similarity_matrix
from Utils.recommendations import (
    recommend_products,
    plot_customer_insights,
    get_simulated_response,
    init_openai_client
)

# Set page config
st.set_page_config(
    page_title="Hyper-Personalization Pro",
    page_icon="🚀",
    layout="wide"
)

@st.cache_resource
def load_all_data():
    """Load and process all data"""
    df = load_data("dataset/sample_data.json")
    processed_df = preprocess_data(df)
    model = load_model()
    embeddings = get_embeddings(processed_df, model)
    similarity_matrix = get_similarity_matrix(embeddings)
    client = init_openai_client()
    return df, processed_df, model, embeddings, similarity_matrix, client

def main():
    st.title("🚀 AI-Driven Hyper-Personalization System")
    st.markdown("""
    **Next-Gen Recommendation Engine**  
    *Combining collaborative filtering with AI-powered insights*
    """)
    
    # Load all data
    df, processed_df, model, embeddings, similarity_matrix, client = load_all_data()
    
    # Sidebar
    with st.sidebar:
        st.header("Customer Selection")
        customer_id = st.selectbox("Select Customer", df["Customer ID"])
        
        st.header("Configuration")
        strategy = st.radio("Recommendation Strategy", 
                          ["Hybrid (Recommended)", "Collaborative Filtering", "Contextual"])
        
        if client:
            st.success("OpenAI Connected")
        else:
            st.info("Using enhanced simulated responses")
    
    # Main content
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("👤 Customer Profile")
        customer_data = df[df["Customer ID"] == customer_id].iloc[0]
        
        st.markdown(f"""
        - **Age:** {customer_data['Age']}
        - **Gender:** {customer_data['Gender']}
        - **Interests:** {', '.join(customer_data['Interests'])}
        - **Engagement Score:** {customer_data['Engagement Score']}/100
        - **Sentiment:** {'😊 Positive' if customer_data['Sentiment Score'] > 0 else '😞 Negative'}
        - **Social Media:** {customer_data['Social Media Activity']}
        """)
        
        st.plotly_chart(plot_customer_insights(customer_data), use_container_width=True)
    
    with col2:
        st.subheader("✨ Recommendations")
        
        if st.button("Generate Recommendations", type="primary"):
            with st.spinner('Analyzing customer data...'):
                tab1, tab2 = st.tabs(["Algorithm Recommendations", "AI Insights"])
                
                with tab1:
                    st.subheader("System Recommendations")
                    recs = recommend_products(
                        customer_id,
                        df,
                        similarity_matrix,
                        strategy.split()[0].lower()
                    )
                    if recs:
                        for item in recs:
                            st.markdown(f"🎯 **{item}**")
                    else:
                        st.info("No recommendations found")
                
                with tab2:
                    st.subheader("AI-Generated Insights")
                    if client:
                        # You would add OpenAI integration here
                        ai_response = get_simulated_response(customer_id)
                    else:
                        ai_response = get_simulated_response(customer_id)
                    
                    st.markdown("#### Product Recommendations")
                    if ai_response.get("products"):
                        for product in ai_response["products"]:
                            st.markdown(f"🌟 **{product['name']}** - {product['reason']}")
                    
                    st.markdown("#### Business Insights")
                    if ai_response.get("insights"):
                        for insight in ai_response["insights"]:
                            st.markdown(f"- {insight}")
                    
                    st.markdown("#### Marketing Messages")
                    if ai_response.get("messages"):
                        for msg in ai_response["messages"]:
                            st.markdown(f'📢 "{msg}"')

if __name__ == "__main__":
    main()