"""
Created on Fri 27 Jan 2023
Dublin, Ireland.

@author: Rafsanjani @rafsanlab

"""
import numpy as np
import os
import shutil
import pathlib
import re
import urllib.request
import zipfile
from natsort import natsorted

def get_data_ftype(path:str, filetype:str, verbose:bool=True, exclude_hidden:bool=True):
  """
  Get files from path with sepsific file types.

  Args:
        path(str): string path containing the files
        file_type(str): file type such as '.png'
        verbose(bool): condition of output summary
  Return:
        paths(list): list of paths
  """

  path = pathlib.Path(path)
  lookfor = '*' + filetype
  paths = list(path.glob(lookfor))
  if exclude_hidden:
      paths = [p for p in paths if not os.path.basename(p).startswith('.')]

    
  paths = sorted(paths)
  if verbose == True:
    print(f'Total paths: {len(paths)}')
  else:
    pass
    
  return paths


def get_fname(filepath, pattern:str, n=3, separator='_'):
    """
    Modify the filename from a_b_c_n.d to a_b_c (if pattern='[._]' and n=3).
    
    Args:
        filepath (str): File path.
        pattern (str): re.split argument i.e: '[._]'.
        n (int): First number of names to be keep.
        separator (str): Name separator for final output.
    
    Return:
        str: Modified filename.
    """
    filepath = pathlib.Path(filepath)
    filename = filepath.parts[-1] 
    filename_parts = re.split(pattern, str(filename))
    modified_filename = ''
    for i in range(n):
        modified_filename += filename_parts[i]
        if i != n-1:
            """ this condition check last filename_parts so that
                no separator at the modified_filename end """
            modified_filename += separator
    # modified_filename = f"{filename_parts[0]}_{filename_parts[1]}_{filename_parts[2]}"
    
    return modified_filename


def get_folder_size(folder_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            total_size += os.path.getsize(filepath)
    return total_size


def get_fonts_in_Colab():
    """ Allow user to install fonts from the URL into Colab. This give option to use custom font
        especially in Matplotlib. Fonts will be rename to fit Colab standard. """
  
    font_dir = '/usr/share/fonts/truetype/san-serif'
    os.makedirs(font_dir, exist_ok=True)
    fonts = [
        ('https://github.com/rafsanlab/etc/raw/main/Fonts/Arial/ARIAL.TTF', 'Arial-Regular.ttf'),
        ('https://github.com/rafsanlab/etc/raw/main/Fonts/Arial/ARIALBD.TTF', 'Arial-Bold.ttf'),
        ('https://github.com/rafsanlab/etc/raw/main/Fonts/Arial/ARIALI.TTF', 'Arial-Italic.ttf')
    ]
    for url, filename in fonts:
        font_path = os.path.join(font_dir, filename)
        urllib.request.urlretrieve(url, font_path)


def create_dir(path:str, verbose=True):
    """
    Function to create directory if not exist.

    Args:
        path(str): path directory.
        verbose(bool): output condition status.
    
    """
    
    path = pathlib.Path(path)
    if os.path.exists(path) == False:
        os.makedirs(path)
        if verbose == True: print('Path created: \t', path)
    elif os.path.exists(path) == True:
        if verbose == True: print('Path already exist.')


def create_project_dir(project_dir='', sub_dirs=[], verbose=True, return_dict=False):
    """
    A function to create a main dir, then sub dirs inside.
    Optional to return dict to the paths usinf sub_dirs as keys.

        """
    # Create main directory
    current_dir = os.getcwd()
    project_dir = os.path.join(current_dir, project_dir)

    # Create subdirectories
    if len(sub_dirs) > 0:
        dirs = {sub_dir: os.path.join(project_dir, sub_dir) for sub_dir in sub_dirs}

    # Create directories
    dirs['project_dir'] = project_dir
    for dir_k, dir_v in dirs.items():

        if os.path.exists(dir_v) == False:
            os.makedirs(dir_v)
            if verbose == True: print('Path created: \t', dir_v)
        elif os.path.exists(dir_v) == True:
            if verbose == True: print('Path exist: \t', dir_v)

    # Return dict
    if return_dict == True:
        return dirs


def copycut_dir(sourcedir, targetdir, verbose=True):
    """
    A function to move contents of source folder/file to target folder.

    """

    if not os.path.exists(sourcedir):
        print(f"sourcedir not exist : '{sourcedir}")
        return

    base_dir = os.path.basename(sourcedir)
    
    # moving sourcedir as a folder 
    if os.path.isdir(sourcedir):

        targetdircut = os.path.join(targetdir, base_dir)
        if not os.path.exists(targetdircut):
            os.makedirs(targetdircut)
            print(f"Created directory : '{targetdircut}")
            
        items = os.listdir(sourcedir) 
        for item in items:
            source_path = os.path.join(sourcedir, item)
            target_path = os.path.join(targetdircut, item)
            shutil.move(source_path, target_path)
            if verbose:
                print(f"Moved '{item}' ->>> '{targetdircut}'")
    
    # moving sourcedir as a file
    else:
        
        if not os.path.exists(targetdir):
            os.makedirs(targetdir)
            print(f"Created directory : '{targetdir}")
        
        shutil.move(sourcedir, targetdir)
        print(f"Moved '{sourcedir}' ->>> '{targetdir}'")


def move_folders_contents(source_directory, target_directory, verbose=True):
    """
    function to move contents of source folder to target folder
    
    Example:
        >>> dir1/content...n
        >>> dir2/content...n

    """
    print('This function will be remove, please use copycut_dir()')
    # Check if both source and target directories exist
    if not os.path.exists(source_directory):
        
        print(f"source_directory not exist : '{source_directory}")
        return
    
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)
        print(f"Create directory : '{target_directory}")

    # Get the list of items (folders and files) in the source directory
    items = os.listdir(source_directory)

    for item in items:
        
        # Construct the full path of the item
        source_path = os.path.join(source_directory, item)
        target_path = os.path.join(target_directory, item)
        shutil.move(source_path, target_path)
        if verbose:
            print(f"Moved '{item}' to '{target_directory}'")

        # # Check if the item is a directory
        # if os.path.isdir(source_path):
        #     # Construct the destination path in the target directory
        #     target_path = os.path.join(target_directory, item)

        #     # Move the entire directory to the target directory
        #     shutil.move(source_path, target_path)
        #     if verbose:
        #         print(f"Moved '{item}' to '{target_directory}'")


def zip_folder(source_folder, output_filename):
    """
    Zip target folder and its contents.

    # Example:
        >>> source_folder = '/content/patches64/train'
        >>> output_filename = '/content/patches64/train' # '/train' here will be 'train.zip'
        >>> zip_folder(source_folder, output_filename)  
    """
    shutil.make_archive(output_filename, 'zip', source_folder)


def unzip_folder(zip_filename, extract_folder):
    """
    Unzip target folder to target output folder.

    # Example:
        >>> zip_filename = '/content/metadata.zip'
        >>> extract_folder = '/content/metadata'
        >>> unzip_folder(zip_filename, extract_folder)
    """
    with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
        zip_ref.extractall(extract_folder)


def match_fname(list1:list, list2:list, method:str='direct',
                split_pattern:str=None, split_n:int=None):
    """
    Match files from two lists by their names.

    Args:
        list1 (list): List of file paths.
        list2 (list): List of file paths.

    Returns:
        file_dict: A dictionary where keys are file names and values are tuples of matching paths from both lists.
    """
    file_dict = {}

    if method=='direct':

        for path1 in list1:
            filename1 = os.path.basename(path1)
            for path2 in list2:
                filename2 = os.path.basename(path2)
                if filename1 == filename2:
                    file_dict[filename1] = (path1, path2)
                    break  #<- once a match is found, no need to continue checking

    elif method=='split' and split_pattern!=None:

        for path1 in list1:
            filename1 = get_filename(path1, split_pattern, split_n)
            for path2 in list2:
                filename2 = get_filename(path2, split_pattern, split_n)
                if filename1 == filename2:
                    file_dict[filename1] = (path1, path2) ##???
                    break

    else:
        print('Either invalide "method" arg (direct or split) of "split_pattern" not specified.')

    return file_dict


def collect_same_file_from_subdir(projectdir, subsubdir=None, fname='', filter_subdir_names:list=None):
    """ collect file paths from subdir of projectdir if all files are the same name.
        returns dict containing the subdir (key) and filepath (value).
    """
    filepaths = {}
    # get all the data from subdir
    for subdir in os.listdir(projectdir):
        if os.path.isdir(os.path.join(projectdir, subdir)): # avoid files, just folders
            if subsubdir is not None: # a subdir of subdir
                filepath = os.path.join(subdir, subsubdir, fname)
            else:
                filepath = os.path.join(subdir, fname)
            filepath = os.path.join(projectdir, filepath)
            if os.path.exists(filepath): # check is exist
                filepaths[subdir] = filepath
    # filter subdir name based on filter_subdir_name list
    if filter_subdir_names is not None:
        filtered_filepaths = {}
        for k, v in filepaths.items():
            if all(name in k for name in filter_subdir_names):
                filtered_filepaths[k] = v
        filepaths = filtered_filepaths
    # natural sort the keys
    filepaths = {k: filepaths[k] for k in natsorted(filepaths)}
    return filepaths
