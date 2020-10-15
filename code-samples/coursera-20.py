import os
def parent_directory():
    # Create a relative path to the parent 
    # of the current working directory 
    relative_parent = os.path.abspath('../')

    # Return the absolute path of the parent directory
    return relative_parent

print(parent_directory())