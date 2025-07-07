import os
import json
import argparse
import matplotlib.pyplot as plt

def load_vectors(input_dir):
    vectors = {}
    for filename in sorted(os.listdir(input_dir)):
        if filename.endswith(".json"):
            clip_id = filename.replace(".json", "")
            with open(os.path.join(input_dir, filename), "r") as f:
                data = json.load(f)
                vectors[clip_id] = data
    return vectors

def plot_vectors(vectors, output_file):
    if not vectors:
        print("No vectors to plot.")
        return

    keys = list(next(iter(vectors.values())).keys())
    keys = [k for k in keys if isinstance(vectors[next(iter(vectors))][k], (int, float))]

    fig, axs = plt.subplots(len(keys), 1, figsize=(10, 2 * len(keys)), sharex=True)
    if len(keys) == 1:
        axs = [axs]

    for i, key in enumerate(keys):
        values = [vectors[k][key] for k in sorted(vectors.keys())]
        axs[i].plot(sorted(vectors.keys()), values, marker='o')
        axs[i].set_title(key)
        axs[i].tick_params(axis='x', rotation=90)

    plt.tight_layout()
    plt.savefig(output_file)
    print(f"✅ Vector plot saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", required=True, help="Path to directory of JSON vector files")
    parser.add_argument("--output_file", required=True, help="Output path for plot image")
    args = parser.parse_args()

    vectors = load_vectors(args.input_dir)
    plot_vectors(vectors, args.output_file)
