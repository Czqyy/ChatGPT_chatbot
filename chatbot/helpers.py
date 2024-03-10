def log_content(path, content):
    """
    Logs content into a text file at `path`. `content` can be a list or string.
    """
    try:
        with open(path, "a") as f:
            if type(content) == list:
                f.writelines(content)
            else:
                f.write(content)
    except IOError as e:
        print(e)