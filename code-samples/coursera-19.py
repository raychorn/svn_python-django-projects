import os
import datetime

def file_date(filename):
    # Create the file in the current directory
    fname = os.path.abspath('./%s' % (filename))
    with open(fname, 'w') as fOut:
        fOut.write('new file')
        fOut.flush()
        fOut.close()
    timestamp = datetime.datetime.fromtimestamp(os.path.getctime(fname))
    # Convert the timestamp into a readable format, then into a string
    s_datetime = timestamp.strftime('%Y-%m-%d')
    # Return just the date portion 
    # Hint: how many characters are in “yyyy-mm-dd”? 
    return ("{}".format(s_datetime))

print(file_date("newfile.txt")) 
# Should be today's date in the format of yyyy-mm-dd