import base64
import streamlit as st
import sqlite3
import streamlit as st
import pandas as pd
from datetime import datetime

conn = sqlite3.connect('bankstatements.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS bankstatements
        (id INTEGER PRIMARY KEY,
        date DATE NOT NULL,
        check INTEGER NOT NULL,
        customercode INTEGER NOT NULL,
        unit INTEGER NOT NULL,
        area INTEGER NOT NULL)''')

conn.commit()
conn.close()