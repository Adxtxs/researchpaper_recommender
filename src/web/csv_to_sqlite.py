import sqlite3
import pandas as pd
from pathlib import Path

# Define project root
project_root = Path(__file__).parent.parent.parent
csv_path = project_root / 'preprocessed_papers.csv'  # Ensure correct CSV filename
db_path = project_root / 'papers.db'

# Load CSV into DataFrame
df = pd.read_csv(csv_path)

# Create SQLite database and store data
conn = sqlite3.connect(db_path)
df.to_sql('papers', conn, if_exists='replace', index=False)
conn.close()

print(f"Database created successfully at {db_path}")
