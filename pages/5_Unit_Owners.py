import base64
import streamlit as st
import sqlite3
import streamlit as st
import pandas as pd
from datetime import datetime

conn = sqlite3.connect('unitowners.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS unitowners
        (id INTEGER PRIMARY KEY,
        customercode INTEGER NOT NULL,
        name TEXT NOT NULL,
        tower INTEGER NOT NULL,
        unit INTEGER NOT NULL,
        area INTEGER NOT NULL)''')

conn.commit()
conn.close()

# connect to database
conn = sqlite3.connect('unitowners.db')
c = conn.cursor()

# create function to add data
def add_data(customercode, name, tower, unit, area):
    c.execute("INSERT INTO unitowners (customercode, name, tower, unit, area) VALUES (?, ?, ?, ?, ?)", (customercode, name, tower, unit, area))
    conn.commit()

# create function to view data
def view_data():
    result = pd.read_sql("SELECT * FROM unitowners", conn)
    return result

# create function to update data
def update_data(customercode, name, tower, unit, area, id):
    c.execute("UPDATE unitowners SET customercode = ?, name = ?, tower = ?, unit = ?, area = ? WHERE id = ?", (customercode, name, tower, unit, area, id))
    conn.commit()

# create function to delete data
def delete_data(id):
    print(f"Deleting unit owner with id={id}")
    try:
        # Delete book from the database
        c.execute(f"DELETE FROM unitowners WHERE id={id}")
        conn.commit()
        st.success("Unit Owner deleted successfully!")
    except Exception as e:
        st.error(f"Error deleting Unit Owner: {e}")
        print(f"Deleted unit owner with id={id}")

# create function to upload data using excel file
def upload_excel(uploaded_file):
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file, engine='openpyxl')
        return df

# create Streamlit app
def main():
    st.title("Unit Owners")

    menu = ["Add Unit Owner", "View Unit Owners", "Update Unit Owner Info", "Delete Unit Owners"]
    choice = st.sidebar.selectbox("Select an option", menu)
    
    if choice == "Add Unit Owner":
        st.subheader("Add New Unit Owner")

        uploaded_file = st.sidebar.file_uploader("Upload Excel", type="xlsx")
        df = upload_excel(uploaded_file)

        if df is not None:
        # Add books from uploaded file
            for i, row in df.iterrows():
                add_data(row["customercode"], row["name"], row["tower"], row["unit"], row["area"])
                st.success("Books added successfully from uploaded file!")
        else:
            customercode = st.number_input("Customer Code")
            name = st.text_input("Name")
            tower = st.number_input("Tower")
            unit = st.number_input("Unit")
            area = st.number_input("Area")
            if st.button("Add Book"):
                add_data(customercode, name, tower, unit, area)
                st.success("Unit Owner Added: {} by {} (Published {})".format(customercode, name, tower, unit, area))
    
    elif choice == "View Unit Owners":
        st.subheader("View Unit Owners")
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
                filename = f"unitowners_{now}.xlsx"
                href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}">Download Excel file</a>'
                st.markdown(href, unsafe_allow_html=True)

    elif choice == "Update Unit Owner Info":
        st.subheader("Update Unit Owner Info")
        result = view_data()
        unitownerlist = result['customercode'].tolist()
        unitownercustomercode = st.selectbox("Select customer code", unitownerlist)
        unitownerdata = result[result['customercode'] == unitownercustomercode]
        newcustomercode = st.number_input("Customer Code", unitownerdata['customercode'].iloc[0])
        newname = st.text_input("Name", unitownerdata['name'].iloc[0])
        newtower = st.number_input("Tower", unitownerdata['tower'].iloc[0])
        newunit = st.number_input("Unit", unitownerdata['unit'].iloc[0])
        newarea = st.number_input("Area", unitownerdata['area'].iloc[0])
        if st.button("Update", key="update"):
            id = unitownerdata['id'].iloc[0]
            update_data(newcustomercode, newname, newtower, newunit, newarea, id)
            st.success("Unit Owner Info Updated!")
    
    elif choice == "Delete Unit Owners":
        st.subheader("Delete Unit Owner")
        result = view_data()
        unitownerlist = result['customercode'].tolist()
        unitownercustomercode = st.selectbox("Select customer code", unitownerlist)
        unitownerdata = result[result['customercode'] == unitownercustomercode]
        if st.button("Delete"):
            id = unitownerdata['id'].iloc[0]
            delete_data(id)
    
if __name__ == '__main__':
    main()