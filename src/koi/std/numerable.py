def is_numerable(value):
    try:
        float(value)
    except ValueError:
        return False
    return True
