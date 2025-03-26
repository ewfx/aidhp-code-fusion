# Import required libraries and modules
import streamlit as st
import pandas as pd
from Utils.data_processing import preprocess_data, load_sample_data
from Utils.embeddings import load_model, get_embeddings, get_similarity_matrix
from Utils.recommendations import recommend_products, recommend_new_customer, plot_customer_insights

# Configure Streamlit page settings
st.set_page_config(
    page_title="Hyper-Personalization Pro",
    page_icon="🚀",
    layout="wide"
)

# Cache resource to load and process data efficiently
@st.cache_resource
def load_all_data():
    # Load and preprocess customer data, generate embeddings and similarity matrix
    df = load_sample_data()
    processed_df = preprocess_data(df)
    model = load_model()
    embeddings = get_embeddings(processed_df, model)
    similarity_matrix = get_similarity_matrix(embeddings)
    return df, processed_df, model, embeddings, similarity_matrix

def main():
    # Set up page title and description
    st.title("🚀 AI-Driven Hyper-Personalization System")
    st.markdown("**Next-Gen Recommendation Engine**  \n*Combining collaborative filtering with AI-powered insights*")
    
    # Load all required data
    df, processed_df, model, embeddings, similarity_matrix = load_all_data()
    
    # Create sidebar for user inputs
    with st.sidebar:
        st.header("Existing Customer Selection")
        customer_name = st.selectbox("Select Customer", df["Customer Name"])
        
        st.header("Configuration")
        strategy = st.radio("Recommendation Strategy", 
                          ["Hybrid (Recommended)", "Collaborative Filtering", "Contextual"])
        
        st.info("Using enhanced simulated responses since API key is not found...!")
    
    # Create two-column layout for customer profile and recommendations
    col1, col2 = st.columns([1, 2])
    
    # Display customer profile in first column
    with col1:
        st.subheader("👤 Existing Customer Profile")
        customer_data = df[df["Customer Name"] == customer_name].iloc[0].to_dict()
        
        # Show customer details in markdown format
        st.markdown(f"- **Age:** {customer_data['Age']}\n- **Gender:** {customer_data['Gender']}\n- **Interests:** {', '.join(customer_data['Interests'])}\n- **Engagement Score:** {customer_data['Engagement Score']}/100\n- **Sentiment:** {'😊 Positive' if customer_data['Sentiment Score'] > 0 else '😞 Negative'}\n- **Social Media:** {customer_data['Social Media Activity']}")
        st.plotly_chart(plot_customer_insights(customer_data), use_container_width=True)
    
    # Display recommendations in second column
    with col2:
        st.subheader("✨ Recommendations for Existing Customer")
        
        # Generate recommendations when button is clicked
        if st.button("Generate Recommendations", type="primary"):
            with st.spinner('Analyzing customer data...'):
                st.subheader("System Recommendations")
                recs = recommend_products(customer_data, df, similarity_matrix, strategy.split()[0].lower())
                if recs:
                    for rec in recs:
                        st.markdown(f"🎯 **{rec['product']}** (Score: {rec['score']:.2f}) - {rec['reason']}")
                else:
                    st.info("No recommendations found")
    
    # Section for new customer recommendations
    st.header("New Customer Recommendation")
    with st.form("new_customer_form"):
        # Form inputs for new customer data
        new_customer_name = st.text_input("New Customer Name", "John Doe")
        new_purchases = st.text_input("Purchase History (comma-separated)", "Tablet, Charger")
        new_sentiment = st.slider("Sentiment Score", -1.0, 1.0, 0.0, key="new_sentiment")
        new_social_activity = st.selectbox("Social Media Activity", ["Low", "Medium", "High"], key="new_social")
        new_age = st.number_input("Age", min_value=18, max_value=100, value=25, key="new_age")
        new_gender = st.selectbox("Gender", ["Male", "Female"], key="new_gender")
        new_interests = st.text_input("Interests (comma-separated)", "Tech, Mobile", key="new_interests")
        new_engagement = st.slider("Engagement Score", 0, 100, 50, key="new_engagement")
        new_submit = st.form_submit_button("Generate New Customer Recommendations")
    
    # Process new customer form submission
    if new_submit:
        new_customer_data = {
            "Customer Name": new_customer_name,
            "Purchase History": [p.strip() for p in new_purchases.split(",")],
            "Sentiment Score": new_sentiment,
            "Social Media Activity": new_social_activity,
            "Age": new_age,
            "Gender": new_gender,
            "Interests": [i.strip() for i in new_interests.split(",")],
            "Engagement Score": new_engagement
        }
        
        with st.spinner('Analyzing new customer data...'):
            new_col1, new_col2 = st.columns([1, 2])
            
            # Display new customer profile
            with new_col1:
                st.subheader("👤 New Customer Profile")
                st.markdown(f"- **Age:** {new_customer_data['Age']}\n- **Gender:** {new_customer_data['Gender']}\n- **Interests:** {', '.join(new_customer_data['Interests'])}\n- **Engagement Score:** {new_customer_data['Engagement Score']}/100\n- **Sentiment:** {'😊 Positive' if new_customer_data['Sentiment Score'] > 0 else '😞 Negative'}\n- **Social Media:** {new_customer_data['Social Media Activity']}")
                st.plotly_chart(plot_customer_insights(new_customer_data), use_container_width=True)
            
            # Display recommendations for new customer
            with new_col2:
                st.subheader("✨ Recommendations for New Customer")
                new_recs = recommend_new_customer(new_customer_data)
                if new_recs:
                    for rec in new_recs:
                        st.markdown(f"🎯 **{rec['product']}** (Score: {rec['score']:.2f}) - {rec['reason']}")
                else:
                    st.info("No recommendations found based on interests")

if __name__ == "__main__":
    main()