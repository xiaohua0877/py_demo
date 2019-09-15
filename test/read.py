import os


def code_lines_count(path):
    code_lines = 0
    comm_lines = 0
    space_lines = 0
    for root, dirs, files in os.walk(path):
        for item in files:
            file_abs_path = os.path.join(root, item)
            postfix = os.path.splitext(file_abs_path)[1]
            if postfix == '.py':
                print("file_abs_path: " + file_abs_path)
                with open(file_abs_path) as fp:
                    while True:
                        line = fp.readline()
                        if not line:
                            break
                        elif line.strip().startswith('#'):
                            comm_lines += 1
                        elif line.strip().startswith("'''") or line.strip().startswith('"""'):
                            comm_lines += 1
                            if line.count('"""') == 1 or line.count("'''") == 1:
                                while True:
                                    line = fp.readline()
                                    comm_lines += 1
                                    if ("'''" in line) or ('"""' in line):
                                        break
                        elif line.strip():
                            code_lines += 1
                        else:
                            space_lines += 1
    return code_lines, comm_lines, space_lines


if __name__ == '__main__':
    abs_dir = os.getcwd()
    x, y, z = code_lines_count(abs_dir)
    print(x, y, z)
