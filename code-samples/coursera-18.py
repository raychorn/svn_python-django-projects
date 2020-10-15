import os

def new_directory(directory, filename):
  # Before creating a new directory, check to see if it already exists
  if os.path.isdir(directory) == False:
    os.mkdir(directory)

  # Create the new file inside of the new directory
  fullname = os.path.join(os.path.abspath('./%s' % (directory)), filename)
  with open (fullname, 'w') as fOut:
    fOut.write('#new file')
    fOut.flush()
    fOut.close()

  # Return the list of files in the new directory
  fdir = os.path.dirname(fullname)
  return [os.path.join(fdir, f) for f in os.listdir(fdir)]

print(new_directory("PythonPrograms", "script.py"))