import streamlit as st
import json
import pandas as pd

# Load & Save Library Data
def load_library():
    try:
        with open("library.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_library():
    with open("library.json", "w") as file: 
        json.dump(library, file, indent=4)  

# Initialize Library
library = load_library()

st.title("Personal Library Manager")
menu = st.sidebar.radio("Select an option", ["View Library", "Add Book", "Remove Book", "Search Book", "Save & Exit"])

if menu == "View Library":
    st.sidebar.header("Your Library")
    if library:
        st.table(library)
    else:
        st.write("No books in your library.Add some books!")

# Add Books
elif menu == "Add Book":  
    st.sidebar.header("Add a new book")
    title = st.text_input("Title")
    author = st.text_input("Author")
    year = st.number_input("Year", min_value=2022, max_value=2100, step=1)
    genre = st.text_input("Genre")
    read_status = st.checkbox("Mark as read")

    if st.button("Add Book"): 
        if title and author and genre:  # Ensure required fields are not empty
            library.append({
                "title": title,
                "author": author,
                "year": year,
                "genre": genre,
                "read_status": read_status
            })
            save_library()

            # Show confirmation message
            st.success("Book added successfully!")
            
            # Show a confirmation prompt
            st.info(f"Book '{title}' by {author} has been added to your library.")

            # Rerun the app to refresh the list
            st.rerun()
        else:
            st.warning("Please fill in all fields before adding a book.")


# Remove Book
elif menu == "Remove Book":
    st.sidebar.header("Remove a book")  
    book_titles = [book["title"] for book in library]

    if book_titles:
        selected_book = st.selectbox("Select a book to remove", book_titles)
        if st.button("Remove Book"):
            library = [book for book in library if book["title"] != selected_book]
            save_library()
            st.success("Book removed successfully!") 
            st.rerun()
    else:
        st.warning("No books in your library. Add some books.")

# Search Book
elif menu == "Search Book": 
    st.sidebar.header("Search a book")  
    search_term = st.text_input("Enter title or author name")
    
    if st.button("Search"):
        results = [book for book in library if search_term.lower() in book["title"].lower() or search_term.lower() in book["author"].lower()]  
        if results:
            st.table(results)
        else:
            st.warning("No book found!")

# Save & Exit
elif menu == "Save & Exit":
    save_library()
    st.success("Library saved successfully!")
