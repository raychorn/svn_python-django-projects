import io

def create_python_script(filename):
    comments = "# Start of a new Python program"
    with open(filename, "w") as fOut:
        fOut.write(comments)
    with open(filename, "r") as fIn:
        filesize = fIn.seek(0, io.SEEK_END)
    return(filesize)

print(create_python_script("program.py"))
