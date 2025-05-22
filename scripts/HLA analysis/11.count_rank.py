import os
import pandas as pd

def count_low_rank_peptides(directory, output_csv):
    results = []
    
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            filepath = os.path.join(directory, filename)
            try:
                df = pd.read_csv(filepath, sep="\t", comment="#")
                if "%Rank_best" in df.columns:
                    count = (df["%Rank_best"] < 10).sum()
                    results.append([filename, count])
                else:
                    print(f"Warning: %Rank_best column not found in {filename}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")
    
    results_df = pd.DataFrame(results, columns=["Filename", "Count<10% Rank"])
    results_df.to_csv(output_csv, index=False)
    print(f"Results saved to {output_csv}")

if __name__ == "__main__":
    directory = "/data/LiuRT/mhc2/MixMHCIIpred/gastric_cancer/prediction/"
    output_csv = "/data/LiuRT/mhc2/MixMHCIIpred/gastric_cancer/prediction/rank_best_counts.csv"
    count_low_rank_peptides(directory, output_csv)
