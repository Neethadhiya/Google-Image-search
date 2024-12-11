import os
import httpx
import streamlit as st
import asyncio
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("api_key")
search_engine_id = os.getenv("search_engine_id")

async def google_search(api_key, search_engine_id, query, **params):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": api_key,
        "cx": search_engine_id,
        "q": query,
        "searchType": "image",
        **params
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        return response.json()

def run_search(api_key, search_engine_id, query):
    results = asyncio.run(google_search(api_key, search_engine_id, query))
    print("API Response:", results)  # Log the API response for debugging
    return results

def main():
    st.title("Google Image Search")
    
    api_key = api_key
    search_engine_id =search_engine_id
    query = st.text_input("Enter product name", "BAKERS BISCUITS NUTTIKRUST")  # Default search query
    # excel_file = st.file_uploader("Upload Excel File", type=["xlsx", "xls"])
    # uploads_dir = "uploads"
    # os.makedirs(uploads_dir, exist_ok=True)
    
    # if excel_file is not None:
    #     # Delete all files in the uploads directory
    #     for filename in os.listdir(uploads_dir):
    #         file_path = os.path.join(uploads_dir, filename)
    #         if os.path.isfile(file_path):
    #             os.remove(file_path)  # Remove the existing file

    #     # Save the uploaded file
    #     file_path = os.path.join(uploads_dir, excel_file.name)
    #     with open(file_path, "wb") as f:
    #         f.write(excel_file.getbuffer())  # Write the new file
        
    #     st.success("File uploaded successfully!")


    if st.button("Search"):
        if api_key and search_engine_id:
            with st.spinner("Searching..."):
                results = run_search(api_key, search_engine_id, query)
                image_links = [item['link'] for item in results.get('items', []) if 'link' in item]
                image_links = image_links[:5]
                if image_links:
                    
                    for link in image_links:
                        st.image(link, use_container_width=True)  # Display images
                        st.markdown(f"<a href='{link}' target='_blank' style='margin: 0; padding: 0;'>{link}</a>", unsafe_allow_html=True)  
                else:
                    st.warning("No images found.")
        else:
            st.error("Please provide both API Key and Search Engine ID.")

if __name__ == "__main__":
    main() 