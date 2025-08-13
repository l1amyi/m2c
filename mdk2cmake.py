import os
import re
from tool import (
    get_c_sources_from_uvprojx,
    get_s_source_from_uvprojx,
    get_libs_from_uvprojx,
    get_defines_from_uvprojx,
    get_includes_from_uvprojx,
    parse_compiler_args,
    filter_compiler_args,
)

def mdk2cmake(uvprojx_path, control_string_path, output_dir=".", tool_chain_path=None):
    uvprojx_path = os.path.abspath(uvprojx_path)
    uvprojx_dir = os.path.dirname(uvprojx_path)
    project_name = os.path.splitext(os.path.basename(uvprojx_path))[0]
    # 解析控制字符串
    c_args = parse_compiler_args(control_string_path, "compiler_control_string")
    asm_args = parse_compiler_args(control_string_path, "assembler_control_string")
    ld_args = parse_compiler_args(control_string_path, "linker_control_string")

    # 过滤-I、--depend、-o、--list、--omf_browse
    filter_keys = ["I", "depend", "o", "list", "omf_browse"]
    c_args = filter_compiler_args(c_args, filter_keys)
    asm_args = filter_compiler_args(asm_args, filter_keys)
    ld_args = filter_compiler_args(ld_args, filter_keys)
    
    # 提取-D宏定义
    def extract_defines(args):
        return [v for k, v in args if k == "D" and v]

    # 提取flags字符串
    def args_to_flags(args, uvprojx_dir):
        flags = []
        for k, v in args:
            if k == "D":
                continue

            v_out = v
            # 判断是否为路径参数
            if v and (v.startswith(".") or v.startswith("/") or v.startswith("\\") or "/" in v or "\\" in v):
                # 去除头尾引号
                if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
                    v = v[1:-1]
                import os
                v_norm = v.replace("\\", "/")
                abs_path = os.path.normpath(os.path.join(uvprojx_dir, v_norm))
                rel_path = os.path.relpath(abs_path, output_dir)
                rel_path = rel_path.replace("\\", "/")
                v_out = "${CMAKE_SOURCE_DIR}/" + rel_path.lstrip("./")
                
                
            if v_out:
                # 若参数包含空格或为路径，加双引号
                if (" " in v_out):
                    v_out = f'"{v_out}"'
                    flags.append(f"-{k}{v_out}" if len(k) == 1 else f"--{k}={v_out}")
                elif ("/" in v_out or "\\" in v_out) and not (v_out.startswith('"') and v_out.endswith('"')):
                    v_out = f'"{v_out}"'
                    flags.append(f"-{k}{v_out}" if len(k) == 1 else f"--{k} {v_out}")
                else:
                    flags.append(f"-{k}{v_out}" if len(k) == 1 else f"--{k}={v_out}")
                
            else:
                flags.append(f"-{k}" if len(k) == 1 else f"--{k}")
        return " ".join(flags)

    cflags = args_to_flags(c_args, uvprojx_dir)
    asmflags = args_to_flags(asm_args, uvprojx_dir)
    ldflags = args_to_flags(ld_args, uvprojx_dir)
    defines = set(extract_defines(c_args) + extract_defines(asm_args) + extract_defines(ld_args))
    

    # 使用tool.py的函数获取分组、库、启动文件
    c_groups = get_c_sources_from_uvprojx(uvprojx_path)
    libs = get_libs_from_uvprojx(uvprojx_path)
    s_file = get_s_source_from_uvprojx(uvprojx_path)
    defines = defines | set(get_defines_from_uvprojx(uvprojx_path))

    def abs2cmake(path):
        # 拼接uvprojx目录，标准化为${CMAKE_SOURCE_DIR}/...
        abs_path = os.path.normpath(os.path.join(uvprojx_dir, path))
        rel_path = os.path.relpath(abs_path, output_dir)
        rel_path = rel_path.replace("\\", "/")
        return "${CMAKE_SOURCE_DIR}/" + rel_path.lstrip("./")

    # include dirs 只用uvprojx中的IncludePath
    raw_incs = get_includes_from_uvprojx(uvprojx_path)
    incs = set()
    for inc in raw_incs:
        abs_path = os.path.normpath(os.path.join(uvprojx_dir, inc))
        rel_path = os.path.relpath(abs_path, output_dir)
        rel_path = rel_path.replace("\\", "/")
        incs.add("${CMAKE_SOURCE_DIR}/" + rel_path.lstrip("./"))
    # 宏定义
    defs = set(defines)
    # 源文件分组
    group_vars = {}
    for g, files in c_groups.items():
        var = g.replace("/", "_").replace(" ", "_").replace("-", "_")
        group_vars[var] = [abs2cmake(f) for f in files]
    # 库
    libs = [abs2cmake(l) for l in libs]
    # 启动文件
    startup_files = []
    if s_file:
        startup_files.append(abs2cmake(s_file))

    # 生成CMakeLists.txt内容
    lines = []
    lines.append("cmake_minimum_required(VERSION 3.12)")
    lines.append(f'set(TOOLCHAIN_PATH "{tool_chain_path}")')
    lines.append('set(CMAKE_C_COMPILER "${TOOLCHAIN_PATH}/armcc.exe")')
    lines.append('set(CMAKE_ASM_COMPILER "${TOOLCHAIN_PATH}/armasm.exe")')
    lines.append('set(CMAKE_C_LINK_EXECUTABLE "${TOOLCHAIN_PATH}/armlinke.exe")')
    lines.append('project("FOC" C)')
    lines.append('enable_language(ASM)')
    if defs:
        defs_str = " ".join(f"-D{d}" for d in defs)
        lines.append(f"add_definitions({defs_str})")
    if cflags:
        cflags_escaped = cflags.replace('\"', '\\"')
        lines.append(f'set(CMAKE_C_FLAGS "${{CMAKE_C_FLAGS}} {cflags_escaped}")')
    if asmflags:
        asmflags_escaped = asmflags.replace('\"', '\\"')
        lines.append(f'set(CMAKE_ASM_FLAGS "${{CMAKE_ASM_FLAGS}} {asmflags_escaped}")')
    if ldflags:
        ld_escaped = ldflags.replace('\"', '\\"')
        lines.append(f'set(USER_LD_FLAGS "{ld_escaped}")')
    if incs:
        lines.append("include_directories(")
        for i in incs:
            lines.append(f"    {i}")
        lines.append(")")
    # 分组变量
    for var, files in group_vars.items():
        if files:
            lines.append(f"set({var}")
            for f in files:
                lines.append(f"    {f}")
            lines.append(")")
    # 启动文件
    if startup_files:
        lines.append("set(STARTUP")
        for f in startup_files:
            lines.append(f"    {f}")
        lines.append(")")
    # 库
    for l in libs:
        lines.append(f'link_libraries("{l}")')
    # 汇总所有源文件
    all_srcs = []
    for files in group_vars.values():
        all_srcs.extend(files)
    if startup_files:
        all_srcs.extend(["${STARTUP}"])
    lines.append(f"add_executable( {project_name} " + " ".join(f"${{{v}}}" for v in group_vars.keys()) + " ${STARTUP})")
    lines.append(f'set_target_properties({project_name} PROPERTIES LINK_FLAGS "${{USER_LD_FLAGS}}")')
    lines.append(f'set_target_properties({project_name} PROPERTIES SUFFIX ".axf")')
    lines.append(f'add_custom_command(TARGET {project_name} POST_BUILD')
    lines.append(f'    COMMAND ${{TOOLCHAIN_PATH}}/fromelf.exe --bin --output {project_name}.bin {project_name}.axf')
    lines.append(f'    COMMAND ${{TOOLCHAIN_PATH}}/fromelf.exe --i32 --output {project_name}.hex {project_name}.axf')
    lines.append('    COMMENT "Generate bin and hex from axf"')
    lines.append(')')
    
    output_path = os.path.abspath(output_dir)
    with open(f"{output_path}/CMakeLists.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

if __name__ == "__main__":
    mdk2cmake("test_data/MDK-ARM/FOC.uvprojx", "test_data/mdk_control_string.txt", "./test_data", "C:/Users/liyi/AppData/Local/Keil_v5/ARM/ARMCC/bin")
