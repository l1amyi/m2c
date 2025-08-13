# coding: utf-8

def parse_compiler_args(filename, section):
    args_list = []
    with open(filename, encoding="utf-8") as f:
        lines = f.readlines()

    # 找到指定段
    in_section = False
    arg_str = ""
    section_tag = f"[{section}]"
    for line in lines:
        line = line.strip()
        if line == section_tag:
            in_section = True
            continue
        if in_section:
            if line.startswith("[") and line.endswith("]"):
                break
            arg_str += " " + line

    import shlex
    tokens = shlex.split(arg_str.strip())

    i = 0
    while i < len(tokens):
        token = tokens[i]
        # --xxx=yyy 形式
        if token.startswith("--") and "=" in token:
            key, value = token[2:].split("=", 1)
            args_list.append([key, value])
        # --xxx yyy 或 --xxx
        elif token.startswith("--"):
            key = token[2:]
            if i + 1 < len(tokens) and not tokens[i + 1].startswith("-"):
                value = tokens[i + 1]
                i += 1
            else:
                value = ""
            args_list.append([key, value])
        elif token.startswith("-"):
            # -Dxxx 形式
            if len(token) > 2 and not token[2] == "=":
                key = token[1]
                value = token[2:]
                args_list.append([key, value])
            # -I xxx 形式
            elif len(token) == 2:
                key = token[1]
                if i + 1 < len(tokens) and not tokens[i + 1].startswith("-"):
                    value = tokens[i + 1]
                    i += 1
                else:
                    value = ""
                args_list.append([key, value])
            else:
                # 其他flag
                key = token.lstrip("-")
                args_list.append([key, ""])
        else:
            # 非参数项，跳过
            pass
        i += 1
    return args_list

import xml.etree.ElementTree as ET

def get_c_sources_from_uvprojx(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    group_dict = {}
    for group in root.iter("Group"):
        group_name_elem = group.find("GroupName")
        if group_name_elem is None or not group_name_elem.text:
            continue
        group_name = group_name_elem.text
        c_files = []
        for file in group.iter("File"):
            type_elem = file.find("FileType")
            path_elem = file.find("FilePath")
            if (
                type_elem is not None and type_elem.text == "1"
                and path_elem is not None and path_elem.text
            ):
                c_files.append(path_elem.text.replace("\\", "/"))
        if c_files:
            group_dict[group_name] = c_files
    return group_dict

def get_s_source_from_uvprojx(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    for group in root.iter("Group"):
        for file in group.iter("File"):
            type_elem = file.find("FileType")
            path_elem = file.find("FilePath")
            if (
                type_elem is not None and type_elem.text == "2"
                and path_elem is not None and path_elem.text
            ):
                return path_elem.text.replace("\\", "/")
    return ""

def get_libs_from_uvprojx(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    libs = []
    for group in root.iter("Group"):
        for file in group.iter("File"):
            type_elem = file.find("FileType")
            path_elem = file.find("FilePath")
            if (
                type_elem is not None and type_elem.text == "4"
                and path_elem is not None and path_elem.text
            ):
                libs.append(path_elem.text.replace("\\", "/"))
    return libs

def get_includes_from_uvprojx(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    includes = set()
    import re
    for inc_elem in root.iter("IncludePath"):
        if inc_elem.text:
            for part in re.split(r"[; ]+", inc_elem.text):
                if part:
                    includes.add(part)
    return [inc.replace("\\", "/") for inc in includes]

def filter_compiler_args(args, filters):
    """
    过滤参数列表，去除k在filters中的项
    :param args: parse_compiler_args返回的参数list
    :param filters: 要过滤的参数名列表，如["I", "depend", "o", "list"]
    :return: 过滤后的参数list
    """
    return [(k, v) for k, v in args if k not in filters]

def get_defines_from_uvprojx(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    defines = set()
    import re
    for define_elem in root.iter("Define"):
        if define_elem.text:
            # 支持分号、逗号、空格分隔
            for part in re.split(r"[;, ]+", define_elem.text):
                if part:
                    defines.add(part)
    return list(defines)

if __name__ == "__main__":
    # 示例调用
    # group_files = get_c_sources_from_uvprojx("MDK-ARM/FOC.uvprojx")
    # for group, files in group_files.items():
    #     print(f"{group}:")
    #     for f in files:
    #         print(f"  {f}")
    # s_file = get_s_source_from_uvprojx("MDK-ARM/FOC.uvprojx")
    # print("s file:", s_file)
    # defines = get_defines_from_uvprojx("MDK-ARM/FOC.uvprojx")
    # print("defines:", defines)
    # libs = get_libs_from_uvprojx("MDK-ARM/FOC.uvprojx")
    # print("libs:", libs)
    # includes = get_includes_from_uvprojx("MDK-ARM/FOC.uvprojx")
    # print("includes:", includes)
    
    # c_args = parse_compiler_args("mdk_control_string.txt", "compiler_control_string")
    asm_args = parse_compiler_args("mdk_control_string.txt", "assembler_control_string")
    # ld_args = parse_compiler_args("mdk_control_string.txt", "linker_control_string")

    # print("C args:", c_args)
    print("ASM args:", asm_args)
    # print("LD args:", ld_args)
