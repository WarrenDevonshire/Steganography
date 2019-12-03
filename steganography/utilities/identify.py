import magic

supported_carry_files = ["image/png"]
supported_hidden_files = ["image/png",
                          "image/jpeg"]


def type_of_file(path):
    return magic.from_file(path, mime=True) in supported_carry_files


def type_of_bin(buffer):
    return magic.from_buffer(buffer, mime=True) in supported_hidden_files
