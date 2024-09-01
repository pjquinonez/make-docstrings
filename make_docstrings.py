import sys


def header_to_docstring(header):
    open_p = header.index("(")
    close_p = header.index(")")
    all_params = (
        header[open_p + 1 : close_p]
        .replace(" ", "")
        .replace("\n", "")
        .replace("\t", "")
    )
    begin = header[:open_p]
    name = begin[3:].replace(" ", "")
    header_split = [x.split(":") for x in all_params.split(",")]
    header_split = [x for x in header_split if hasattr(x, "__len__") and len(x) == 2]
    # TODO: fakebugwebsite.com/555 - Include scenarios where there are multiple datatypes. Ex: Callable[[int], bool]

    final_txt = (
        '"""___one_sentence_summarry_of_'
        + name
        + "___\n\n"
        + "___multi_line_summary_of_"
        + name
        + "___\n\n"
        + "Args:\n"
    )
    for param in header_split:
        final_txt = (
            final_txt
            + "\t"
            + param[0]
            + " ("
            + param[1]
            + "):\n"
            + "\t\t___summary_of_"
            + param[0]
            + "___\n"
        )
    final_txt = final_txt + "Returns:\n\t___summary_of_" + name + '_returns___"""\n'
    return final_txt


def get_file_txt(path):
    f = open(path, "r")
    final_txt = f.read()
    f.close()
    return final_txt


def get_all_headers(file_txt):
    k = 0
    last = 0
    txt_list = []
    while k <= len(file_txt):
        if file_txt[k - 1 : k + 1] == "):" or file_txt[k - 1 : k + 1] == "->":
            if file_txt[k - 1 : k + 1] == "->":
                while file_txt[k] != ":":
                    k = k + 1
            txt_list = txt_list + [file_txt[last : k + 1]]
            last = k + 1
        k = k + 1
    txt_list = ["def " + x.split("def ")[-1] for x in txt_list if "def " in x]
    return txt_list


def main():
    path = "./big-morpheus/src/models/train_model.py"
    txtfile_path = "./method_docstrings.txt"
    py_txt = get_file_txt(path)
    all_headers = get_all_headers(py_txt)
    txtfile_txt = "\n*********************************\n".join(
        [header_to_docstring(x) for x in get_all_headers(py_txt)]
    )
    f = open(txtfile_path, "w")
    f.write(txtfile_txt)
    f.close()


if __name__ == "__main__":
    main()
