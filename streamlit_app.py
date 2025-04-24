import streamlit as st
import os
import json
from src.chatbot.processing import process_message, load_product_catalog, get_store_details

# Set page config
st.set_page_config(
    page_title="Interactly - AI Customer Service",
    page_icon="🤖",
    layout="wide"
)

def initialize_session_state():
    """Initialize session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "selected_store" not in st.session_state:
        st.session_state.selected_store = None
    if "selected_product" not in st.session_state:
        st.session_state.selected_product = None

def load_product_catalog():
    """Load product catalog from JSON file."""
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    catalog_file = os.path.join(data_dir, "product_catalog.json")
    
    try:
        with open(catalog_file, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        st.error("Product catalog not found!")
        return {"stores": []}

def get_store_details(store_name, catalog):
    """Get detailed information about a specific store."""
    for store in catalog["stores"]:
        if store["name"].lower() == store_name.lower():
            return store
    return None

def get_product_details(store_name, product_name, catalog):
    """Get detailed information about a specific product within a store."""
    store = get_store_details(store_name, catalog)
    if store:
        for product in store["products"]:
            if product["name"].lower() == product_name.lower():
                return product
    return None

def main():
    # Initialize session state
    initialize_session_state()

    # Load product catalog
    catalog = load_product_catalog()
    stores = [store["name"] for store in catalog["stores"]]

    # Sidebar for store and product selection
    with st.sidebar:
        st.title("Store Selection")
        selected_store = st.selectbox(
            "Select a Store",
            stores,
            index=stores.index(st.session_state.selected_store) if st.session_state.selected_store in stores else 0
        )

        # Update selected store in session state
        if selected_store != st.session_state.selected_store:
            st.session_state.selected_store = selected_store
            st.session_state.selected_product = None
            st.session_state.messages = []

        # Get products for selected store
        store_details = get_store_details(selected_store, catalog)
        if store_details:
            products = [product["name"] for product in store_details["products"]]
            selected_product = st.selectbox(
                "Select a Product",
                ["All Products"] + products,
                index=0
            )
            st.session_state.selected_product = selected_product if selected_product != "All Products" else None

    # Main content area
    st.title("Interactly - AI Customer Service")
    
    # Chat interface
    st.subheader("Chat with our AI Assistant")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Chat input
    if prompt := st.chat_input("What would you like to know?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.write(prompt)
        
        # Generate and display assistant response
        with st.chat_message("assistant"):
            response = process_message(
                prompt,
                st.session_state.selected_store,
                st.session_state.selected_product
            )
            st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main() 