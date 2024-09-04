import argparse
import os
import sys

# TODO: Make work for class methods


def header_to_docstring(header: str):
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
    # TODO: Include scenarios where there are multiple datatypes. Ex: Callable[int, bool]

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
    final_txt = final_txt + "Returns:\n\t___summary_of_" + name + '_returns___"""'
    final_txt = (
        final_txt
        + "\n# TODO: Document summary of "
        + name
        + " function\n"
        + "\n".join(
            ["# TODO: Document " + param[0] + " parameter" for param in header_split]
        )
    )
    return final_txt


def get_file_txt(path: str):
    f = open(path, "r")
    final_txt = f.read()
    f.close()
    return final_txt


def get_all_headers(file_txt: str):
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


def get_filename(file_path: str):
    file = os.path.basename(file_path)
    file_name = file[: file.index(".")]
    return file_name


def main(input_path: str, output_path: str):
    if not output_path:
        output_path = "./"
    output_file_path = os.path.join(
        output_path, get_filename(input_path) + "_method_docstrings.txt"
    )

    py_txt = get_file_txt(input_path)
    all_headers = get_all_headers(py_txt)
    txtfile_txt = "\n*********************************\n".join(
        [header_to_docstring(x) for x in get_all_headers(py_txt)]
    )
    f = open(output_file_path, "w")
    f.write(txtfile_txt)
    f.close()
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create txt file including docstring templates"
    )
    parser.add_argument("input", help="path for input file")
    parser.add_argument(
        "-o", "--output", metavar="", help='path for output file, "./" if None'
    )
    args = parser.parse_args()
    main(input_path=args.input, output_path=args.output)
