import re
import os
import argparse
from multiprocessing import Pool

def feat_parallel(args):
    fsfLoc = args.fsf

    with open(fsfLoc, 'r') as f:
        text = f.read()

    text = re.sub('set fmri\(multiple\)\s+(\d+)', '1', text)

    fMRI_data_list = re.findall('\
# 4D AVW data or FEAT directory \(\d+\)\n\
set feat_files\(\d+\)\s+\"(\S.+)\"\n', text)

    fMRI_lineNum = text.index('# 4D AVW data or FEAT directory')

    #fMRI line removal
    text = re.sub('# 4D AVW data or FEAT directory \(\d+\)\n\
set feat_files\(\d+\).+\n\n', "", text)

    for fMRI_img in fMRI_data_list:
        #newText = text[:fMRI_lineNum] + 
        fMRI_insert = '# 4D AVW data or FEAT directory (1)\n\
set feat_files(1) "{0}"\n\n'.format(fMRI_img)
        fMRI_edited_text = text[:fMRI_lineNum] + fMRI_insert + text[fMRI_lineNum:]


    sMRI_lineNum = fMRI_edited_text.index('# Subject\'s structural image for analysis')
    sMRI_data_list = re.findall('\
# Subject\'s structural image for analysis \d+\n\
set highres_files\(\d+\)\s+\"(\S.+)\"\n', fMRI_edited_text)

    # sMRI line removal
    fMRI_edited_text = re.sub('# Subject\'s structural image for analysis \d+\n\
set highres_files\(\d+\)\s+\"(\S.+)\"\n\n', "", fMRI_edited_text)

    for sMRI_img in sMRI_data_list:
        #newText = text[:fMRI_lineNum] + 
        sMRI_insert = '# Subject\'s structural image for analysis 1\n\
set highres_files(1) "{0}"\n\n'.format(sMRI_img)
        final_text = fMRI_edited_text[:sMRI_lineNum] + sMRI_insert + fMRI_edited_text[sMRI_lineNum:]


    print final_text
                    



    newLine = '# 4D AVW data or FEAT directory \(1)\nset feat_files\(\d+\).+\n'
    #print text



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parallizes the feat')

    parser.add_argument('--fsf','-f', 
                        help='Feat configuration file saved with multiple subjects')

    args = parser.parse_args()
    feat_parallel(args)
