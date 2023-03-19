import base64
import streamlit as st
import sqlite3
import streamlit as st
import pandas as pd
from datetime import datetime

conn = sqlite3.connect('example.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS books
        (id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        year INTEGER NOT NULL)''')

conn.commit()
conn.close()

# connect to database
conn = sqlite3.connect('example.db')
c = conn.cursor()

# create function to add data
def add_data(title, author, year):
    c.execute("INSERT INTO books (title, author, year) VALUES (?, ?, ?)", (title, author, year))
    conn.commit()

# create function to view data
def view_data():
    result = pd.read_sql("SELECT * FROM books", conn)
    return result

# create function to update data
def update_data(title, author, year, id):
    c.execute("UPDATE books SET title = ?, author = ?, year = ? WHERE id = ?", (title, author, year, id))
    conn.commit()

# create function to delete data
def delete_data(id):
    c.execute("DELETE FROM books WHERE id = ?", (id,))
    conn.commit()

# create Streamlit app
def main():
    st.title("Book Manager")
    
    menu = ["Add Book", "View Books", "Update Book", "Delete Book"]
    choice = st.sidebar.selectbox("Select an option", menu)
    
    if choice == "Add Book":
        st.subheader("Add New Book")
        title = st.text_input("Title")
        author = st.text_input("Author")
        year = st.number_input("Year Published")
        if st.button("Add Book"):
            add_data(title, author, year)
            st.success("Book Added: {} by {} (Published {})".format(title, author, year))
    
    elif choice == "View Books":
        st.subheader("View Books")
        result = view_data()
        st.write(result)
    
        # Add "Export to Excel" button
        if st.button("Export to Excel"):
            # Use pandas to write table to Excel file
            result.to_excel("books.xlsx", index=False)
            st.success("Table exported to Excel file 'books.xlsx'")
    
            # Generate download link for Excel file
            with open("books.xlsx", "rb") as f:
                file = f.read()
                b64 = base64.b64encode(file).decode()
                now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                filename = f"books_{now}.xlsx"
                href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}">Download Excel file</a>'
                st.markdown(href, unsafe_allow_html=True)

    elif choice == "Update Book":
        st.subheader("Update Book")
        result = view_data()
        booklist = result['title'].tolist()
        booktitle = st.selectbox("Select a book", booklist)
        bookdata = result[result['title'] == booktitle]
        newtitle = st.text_input("Title", bookdata['title'].iloc[0])
        newauthor = st.text_input("Author", bookdata['author'].iloc[0])
        newyear = st.number_input("Year Published", bookdata['year'].iloc[0])
        if st.button("Update", key="update"):
            id = bookdata['id'].iloc[0]
            update_data(newtitle, newauthor, newyear, id)
            st.success("Book Updated!")
    
    elif choice == "Delete Book":
        st.subheader("Delete Book")
        result = view_data()
        booklist = result['title'].tolist()
        booktitle = st.selectbox("Select a book", booklist)
        bookdata = result[result['title'] == booktitle]
        if st.button("Delete"):
            id = bookdata['id'].iloc[0]
            delete_data(id)
            st.success("Book Deleted: {}".format(booktitle))
    
if __name__ == '__main__':
    main()

# hide streamlit menu and footer
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)