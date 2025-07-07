import os
import sys
import json
import pandas as pd

def load_vectors(input_dir):
    data = []
    for fname in sorted(os.listdir(input_dir)):
        if fname.endswith('.json'):
            path = os.path.join(input_dir, fname)
            with open(path, 'r') as f:
                vector = json.load(f)
                vector['filename'] = fname
                data.append(vector)
    return pd.DataFrame(data)

if __name__ == "__main__":
    input_dir = sys.argv[sys.argv.index('--input_dir') + 1]
    df = load_vectors(input_dir)

    # Print summary statistics
    print("\n📊 Emotion Vector Stats (mean ± std):\n")
    print(df.describe(include='all'))

    # Optional: Save CSV for Excel/Numbers
    out_csv = os.path.join(input_dir, 'vector_summary.csv')
    df.to_csv(out_csv, index=False)
    print(f"\n✅ Vector summary saved to {out_csv}")
