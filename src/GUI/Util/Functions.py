

def clean_name_for_file(name):
    OK_LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_"
    name_new = ""
    for letter in name:
        if letter not in OK_LETTERS:
            name_new += "_"
        else:
            name_new += letter
    return name_new
