import os
import httpx
import streamlit as st
import asyncio
import pandas as pd
import io  
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
    return results

def main():
    st.title("Google Image Search")
    api_key = api_key
    search_engine_id =search_engine_id
    excel_file = st.file_uploader("Upload Excel File", type=["xlsx", "xls"])
    uploads_dir = "uploads"
    os.makedirs(uploads_dir, exist_ok=True)
    
    if excel_file is not None:
        # Delete all files in the uploads directory
        for filename in os.listdir(uploads_dir):
            file_path = os.path.join(uploads_dir, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)  # Remove the existing file

        # Save the uploaded file
        
        file_path = os.path.join(uploads_dir, excel_file.name)
        with open(file_path, "wb") as f:
            f.write(excel_file.getbuffer())  # Write the new file
        df = pd.read_excel(file_path, engine='openpyxl')  # For .xlsx files
        print(df.columns.tolist(),"-------------------")
        print(f"File name: {excel_file.name}, File type: {excel_file.type}, File size: {excel_file.size}")

        if st.button("Add Image URL"):
            df = pd.read_excel(file_path, engine='openpyxl', sheet_name=0)  # Reads the first sheet
            image_urls = []  
            for description in df['Description']:  # Assuming the column with descriptions is named 'Description'
                results = run_search(api_key, search_engine_id, description)  # Search for each description
                image_links = [item['link'] for item in results.get('items', [])]
                image_urls.append(image_links[0] if image_links else None)  # Store the first image URL or None

            # Add a new column for image URLs in the DataFrame
            df['Image URL'] = image_urls

            # Save the updated DataFrame to a BytesIO object
            output = io.BytesIO()
            df.to_excel(output, index=False)  # Save the updated file to the BytesIO object
            output.seek(0)  # Move to the beginning of the BytesIO object

            # Create a download button for the updated Excel file
            st.download_button(
                label="Download Updated Excel File",
                data=output,
                file_name="updated_" + excel_file.name,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

            # Create a button to add image URL
        
            # Logic to add image URL can be implemented here
            st.write("Image URL added!")  # Placeholder for actual functionality

if __name__ == "__main__":
    main() 