import pandas as pd

csv_path = 'assets/data/imagenette/4700/samples.csv'

# Read the CSV
df = pd.read_csv(csv_path)

# Reduce to 4700 rows
df = df.head(4700)  # Keeps only the first 4700 rows

# Save back as CSV
df.to_csv(csv_path, index=False)


