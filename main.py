import os

def check_file_ext(file):
    #print("current file is:", file)
    if file.endswith(".h") or file.endswith(".c") and file.count(".") == 1:
        return True
    else:
        return False

def add_enter_str():
    return "{pr_err(\"enter :%s, %d\\n\", __func__, __LINE__);\n"
def add_exit_str():
    return "pr_err(\"exit :%s, %d\\n\", __func__, __LINE__);}\n"
def add_mid_exit_str():
    return "pr_err(\"exit :%s, %d\\n\", __func__, __LINE__);\n"

def process_file(file):
    print("proceeded file is:", file)
    handle = open(file, "r")
    replacement = ""
    line = handle.readline()
    # this check is not precise, but enough for most files
    has_left = False
    while line:
        if len(line.strip()) == 1 and line[0] == "{":
            line = add_enter_str()
            has_left = True
            replacement = replacement + line
            line = handle.readline()
        elif has_left:
            cur = line
            line = handle.readline()
            if len(cur) == 1 and cur[0] == "}":
                replacement = replacement + add_exit_str()
                has_left = False
            elif line and line[0] == "}" and "return" in cur:
                replacement = replacement + add_mid_exit_str()
                replacement = replacement + cur
                replacement += "}\n"
                has_left = False
                line = handle.readline()
            else:
                replacement = replacement + cur
        else:
            replacement = replacement + line
            line = handle.readline()

    handle.close()

    handle = open(file, "w")
    handle.write(replacement)
    handle.close()

def process_files(file_folder):
    os.chdir(file_folder)
    for dirpath, dirnames, filenames in os.walk(os.getcwd()):
        #print("dirpath {} dirnames {}".format(dirpath, dirnames))
        for item in filenames:
            if check_file_ext(item):
                process_file(dirpath + "/"  + item)


if __name__ == "__main__":
    file_folder = "."
    process_files(file_folder)
