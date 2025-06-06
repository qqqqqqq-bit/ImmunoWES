import os
import pandas as pd

def find_divergence_files(base_path):
    """Recursively find all files containing IndividualDivergence"""
    divergence_files = []
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if 'IndividualDivergence' in file and file.endswith('.txt'):
                full_path = os.path.join(root, file)
                divergence_files.append(full_path)
    return divergence_files

def process_divergence_files(base_path):
    # Find all relevant files
    all_files = find_divergence_files(base_path)
    
    # Store data for all files
    all_data = {}
    file_names = []
    
    # Process each file
    for file_path in all_files:
        # Get the file name as column name
        file_name = os.path.basename(file_path)
        file_names.append(file_name)
        
        try:
            # Read the file, only read the first and third columns
            data = []
            with open(file_path, 'r') as f:
                # Skip the header row
                next(f)
                for line in f:
                    parts = line.strip().split('\t')
                    if len(parts) >= 3:  # Make sure there are at least 3 columns on the row
                        id_val = parts[0]
                        div_val = parts[2]
                        try:
                            # Convert divergence value to floating point number
                            div_val = float(div_val)
                            data.append((id_val, div_val))
                        except ValueError:
                            continue
            
            # Create a mapping of ID to Divergence_Average
            all_data[file_name] = dict(data)
            
        except Exception as e:
            print(f"Error processing file {file_name}: {str(e)}")
            continue
    
    # Get all unique IDs
    all_ids = set()
    for data in all_data.values():
        all_ids.update(data.keys())
    
    # Create a result DataFrame
    result_data = []
    
    # Create one row of data for each ID
    for eid in sorted(all_ids):
        row = {'eid': eid}
        # Add the corresponding Divergence_Average value in each file
        for file in sorted(file_names):
            row[file] = all_data[file].get(eid, '')  # Use empty string if there is no value
        result_data.append(row)
    
    # Create a DataFrame
    result_df = pd.DataFrame(result_data)
    
    # Make sure eid is listed first
    columns = ['eid'] + sorted([col for col in result_df.columns if col != 'eid'])
    result_df = result_df[columns]
    
    # Save as CSV to ensure the digital format remains the same
    output_path = os.path.join(base_path, 'combined_divergence.csv')
    result_df.to_csv(output_path, index=False, float_format='%.11f')
    
    print(f"Processing is complete. A total of {len(file_names)} files were processed, including {len(all_ids)} unique IDs.")
    print(f"The output file is saved in: {output_path}")
    print("\nExamples of the first few lines of data：")
    print(result_df.head().to_string())

# Example of usage
base_path = '/data/yuan/gastric_cancer/hla_estimation'
process_divergence_files(base_path)
