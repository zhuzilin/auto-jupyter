import nbformat as nbf
import os
import numpy as np
import pandas as pd
import fire

def add(nb, source, type):
    """assisting function to simplified the code for adding cell to notebook
    """
    if nb['cells'] is None:
        nb['cells'] = []
    type = type.lower()
    if type == 'md' or type == 'markdown':
        nb['cells'].append(nbf.v4.new_markdown_cell(source))
    elif type == 'code':
        nb['cells'].append(nbf.v4.new_code_cell(source))

def read_file(input_dir, file_type):
    """function to generate read file code for jupyter notebook
        and also read the file locally for further analysis
    """
    if file_type == 'json':
        read_code = "df = pd.read_json(r'{}')".format(input_dir)
        df = pd.read_json(input_dir)
    elif file_type == 'csv':
        read_code = "df = pd.read_csv(r'{}')".format(input_dir)
        df = pd.read_csv(input_dir)
    return read_code, df

def check_data_type():
    code = r"""# check data types
for column in df.columns.values:
    line = 'Column: {} '.format(column)
    if type(df[column][0]) == list:
        line += 'list of {}'.format(str(type(df[column][0][0])))
    else:
        line += str(type(df[column][0])) + '\nExamples: ' + str(df[column][0])
    print(line)
"""
    return code

class auto_jupyter:

    def create(self, input_dir, **kwargs):
        """ the main function to generate the notebook
        """
        # make sure valid input
        input_dir = os.path.abspath(input_dir)
        file_name = os.path.basename(input_dir)
        name, file_type = file_name.split('.')
        assert file_type in ['json', 'csv'], "Wrong input file type!"
        assert os.path.exists(input_dir), "No such file"
        
        # create new notebook
        nb = nbf.v4.new_notebook()
        nb['cells'] = []
        
        # header cell
        if 'name' in kwargs:
            name = kwargs['name']
        else:
            name = os.path.basename(input_dir).split('.')[0]
        header = "# Basic Analysis of {}".format(name.lower().capitalize())
        add(nb, header, 'md')
        
        # import cell
        import_code = r"""# import packages
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
%matplotlib"""
        nb['cells'].append(nbf.v4.new_code_cell(import_code))
        
        # read data
        read_code, df = read_file(input_dir, file_type)
        add(nb, read_code, 'code')
        
        # raw analysis
        add(nb, "df.info()", 'code')
        add(nb, "df.head()", 'code')
        add(nb, check_data_type(), 'code')
        
        # output notebook
        if 'output' in kwargs:
            output = kwargs['output']
        else:
            tmp_dir_list = input_dir.split('\\')
            output = os.path.join(tmp_dir_list[0], os.sep, *(tmp_dir_list[1:-1]))  # for compatible with Windows and Linux
        if not os.path.exists(output):
            os.mkdir(output)
        nbf.write(nb, os.path.join(output, '{}.ipynb'.format(name)))
    
if __name__ == '__main__':
    fire.Fire(auto_jupyter);