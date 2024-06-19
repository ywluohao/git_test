import pandas as pd

# Sample data
data = {
    'org': ['a|aa|sd|s', 'x|y|z', 'foo|bar|baz', '', 'test'],
    'path': ['a|aa|sd|e', 'x|y|a', 'foo|bar|qux', 'some', '']
}

# Create DataFrame
df = pd.DataFrame(data)

# Function to convert the string to a list
def convert_to_list(s):
    if pd.isnull(s) or s == '':
        return []
    return s.split('|')

# Function to find the common and different parts of two lists
def find_common_and_diff(org_str, path_str):
    org = convert_to_list(org_str)
    path = convert_to_list(path_str)
    
    if not org or not path:
        return [], org, path

    min_len = min(len(org), len(path))
    common_prefix = []
    for i in range(min_len):
        if org[i] == path[i]:
            common_prefix.append(org[i])
        else:
            break

    # The different parts are the lists after the common prefix
    common_len = len(common_prefix)
    org_diff = org[common_len:]
    path_diff = path[common_len:]

    return common_prefix, org_diff, path_diff

# Apply the function to each row in the DataFrame
df[['common', 'org_diff', 'path_diff']] = df.apply(
    lambda row: pd.Series(find_common_and_diff(row['org'], row['path'])), 
    axis=1
)

# Display the result
print(df)