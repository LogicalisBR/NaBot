import os


def serve_file(filename, text):
    print(f"Saving temporary file as: {filename}")
    with open(filename, 'w') as f:
        f.write(text)
        return os.path.abspath(filename)
