import pandas as pd
import os

def evaluate_rule(row_value, rule_value):
    rule_value = rule_value.replace('(', '').replace(')', '').strip()
    if '>' in rule_value:
        value = float(rule_value.split('>')[-1].strip())
        return row_value > value
    elif '<=' in rule_value:
        value = float(rule_value.split('<=')[-1].strip())
        return row_value <= value
    return False

def match_rules_to_rows(data_df, rules_df):
    matched_rows = []
    for i, row in data_df.iterrows():
        matched_rules = []
        matched_rule_strings = set() 

        for j, rule_row in rules_df.iterrows():
            rule = ""
            rule_length = 0
            is_matched = True
            for col_name, rule_value in rule_row.items():
                if pd.notna(rule_value):
                    if col_name != 'class':
                        if evaluate_rule(row[col_name], rule_value):
                            rule += f"{rule_value} && "
                            rule_length += 1
                        else:
                            is_matched = False
                            break
                    else:
                        if str(row['class']) != str(rule_value):
                            is_matched = False
                            break
            if is_matched and rule_length > 0:
                matched_rule_strings.add(rule)
                matched_rules.append({'Rule': rule[:-4] + f" => {rule_row['class']}", 'Rule Length': rule_length})
    
        if matched_rules:
            matched_rows.append({'Row Number': i + 1, 'Matched Rules': matched_rules})
    
    matched_rows_df = pd.DataFrame(matched_rows)
    matched_rows_df['Matched Rules'] = matched_rows_df['Matched Rules'].apply(lambda x: tuple(x))
    matched_rows_df = matched_rows_df.join(pd.DataFrame(matched_rows_df['Matched Rules'].tolist()))
    
    return matched_rows_df

base_rules_folder = 'subtable_'
output_folder = 'subtable_'
os.makedirs(output_folder, exist_ok=True)


for i in range(1, 6):
    csv_file_data = os.path.join(f"{base_rules_folder}{i}", f"2consistent_modified_lymphography{i}.csv")
    csv_file_rules = os.path.join(f"{base_rules_folder}{i}", f"3decision_rules_{i}.csv")
    
    data_df = pd.read_csv(csv_file_data, header=0)
    rules_df = pd.read_csv(csv_file_rules, header=0)

    matched_rows = match_rules_to_rows(data_df, rules_df)
    
    output_file = os.path.join(f'{output_folder}{i}', f"4matched_rows_{i}.csv")
    matched_rows.to_csv(output_file, index=False)

print("Dopasowanie reguł zakończone sukcesem.")
