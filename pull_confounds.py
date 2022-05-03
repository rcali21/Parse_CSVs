import os 
import pandas as pd
import glob



path1 = input('Specify path to fMRI_prep dir:')
os.chdir(path1)

# Intialize empty list for subject paths to be appended to 
path_list = []

# Glob to locate .tsv files
for x in glob.glob('sub*/ses-1/func/'):
    y = os.listdir(x)

    for item in y:
        if item.endswith('.tsv'):
            # Append path to each .tsv file to list
            path_list.append(os.path.join(path1, x, item))


# Initialize empty df to append to 

output_df = pd.DataFrame()

#Initialize empty lists to append means from each subject to
sub_list = []
fd_list = []
dvars_list = []
rmsd_list = []
bold_vols_list = []

# Iterate over subject paths, find each of their .tsv files, and read them in
for target in path_list:
    func_dirs = os.path.dirname(target)
    dirs_stripped = os.path.dirname(os.path.dirname(func_dirs))
    sub_id = os.path.basename(dirs_stripped)
    sub_list.append(sub_id)
    df = pd.read_csv(target, sep='\t')
    # Locate desired columns and calculate the means for each
    r = df["framewise_displacement"].mean()
    a = df["dvars"].mean()
    t = df["rmsd"].mean()
    # Count how many rows there are and assign that to bold_vols
    bold_vols = len(df.index)
    # Append each mean for each subject to a list
    fd_list.append(r)
    dvars_list.append(a)
    rmsd_list.append(t)
    bold_vols_list.append(bold_vols)

# Add columns and populate columns with items from each list that we generated in the last step
output_df["Subject_ID"] = sub_list
output_df["Framewise_Displacement"] = fd_list
output_df["DVARS"] = dvars_list
output_df["RMSD"] = rmsd_list
output_df["BOLD_Volumes"] = bold_vols_list

# Specify output .csv filename 
output_file = input('Specify desired filename for csv:')

# Save to .csv
output_df.to_csv(output_file, sep='\t', encoding='utf-8')

