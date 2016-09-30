import re
import os
import argparse
from multiprocessing import Pool

def feat_parallel(args):
    fsfLoc = args.fsf

    with open(fsfLoc, 'r') as f:
        text = f.read()

    text = text.replace('set fmri(featwatcher_yn) 1',
                  'set fmri(featwatcher_yn) 0')

    text = re.sub('set fmri\(multiple\) \d+', 
                  'set fmri(multiple) 1', text)

    fMRI_data_list = re.findall('\
# 4D AVW data or FEAT directory \(\d+\)\n\
set feat_files\(\d+\)\s+\"(\S.+)\"\n', text)

    fMRI_lineNum = text.index('# 4D AVW data or FEAT directory')

    #fMRI line removal
    text = re.sub('\
# 4D AVW data or FEAT directory \(\d+\)\n\
set feat_files\(\d+\).+\n\n', "", text)

    sMRI_lineNum = text.index("# Subject's structural image for analysis")
    sMRI_data_list = re.findall('\
# Subject\'s structural image for analysis \d+\n\
set highres_files\(\d+\)\s+\"(\S.+)\"\n', text)

    # sMRI line removal
    text = re.sub('\
# Subject\'s structural image for analysis \d+\n\
set highres_files\(\d+\)\s+\"(\S.+)\"\n\n', "", text)

    new_fsf_list = []
    for fMRI_img, sMRI_img in zip(fMRI_data_list, sMRI_data_list):
        #newText = text[:fMRI_lineNum] + 
        fMRI_insert = '\
# 4D AVW data or FEAT directory (1)\n\
set feat_files(1) "{0}"\n\n'.format(fMRI_img)
        fMRI_edited_text = text[:fMRI_lineNum] + fMRI_insert + text[fMRI_lineNum:]

        sMRI_insert = '\
# Subject\'s structural image for analysis 1\n\
set highres_files(1) "{0}"\n\n'.format(sMRI_img)
        new_sMRI_lineNum = sMRI_lineNum + len(fMRI_insert)

        final_text = fMRI_edited_text[:new_sMRI_lineNum] + sMRI_insert + fMRI_edited_text[new_sMRI_lineNum:]
        
        targetText = os.path.join(os.path.dirname(args.fsf),
                                  re.sub('\/','_', fMRI_img)+'.fsf')
        new_fsf_list.append(targetText)

    return new_fsf_list
        #with open(targetText, 'w') as f:
            #f.write(final_text)

        #os.popen('feat {0}'.format(targetText)).read()



def feat(fsf):
    return os.popen('feat {0}'.format(fsf)).read()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parallizes the feat')

    parser.add_argument('--fsf','-f', 
                        help='Feat configuration file saved with multiple subjects')
    parser.add_argument('--j','-j', 
                        help='Number of cores to use')

    args = parser.parse_args()
    new_fsf_list = feat_parallel(args)

    pool = Pool(processes = args.j)
    print pool.map(feat_parallel, new_fsf_list)
    print 'Completed'
