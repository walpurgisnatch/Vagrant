def write_line(fname, data):
    with open(fname, 'a') as f:
        f.write(data + "\n")

def read_by_line(fname):
    with open(fname, 'r') as f:
        for line in f:
            yield line

def read_file(fname):
    with open(fname, 'r') as f:
        return f.read()
