def parse_lines(lines, output_file, functions):
    """
    Parse a test description file and produce a JSON config and a Python script.
    :param lines: The lines to be parsed.
    :param output_file: The output file name.
    :param functions: The function names.
    :return: A corresponding JSON config and Python script.
    """
    config = dict()
    config['name'] = output_file.replace("_", " ")
    config['devices'] = []
    config['experiment'] = [{
                  "type": "PY_SCRIPT",
                  "source": output_file + ".py",
                  "order":  1
                },
                {
                    "type": "PY_SCRIPT",
                    "source": "CustomTestReduce.py",
                    "order": 2
                }
    ]
    config['data'] = {}
    script = "import time\n" + \
        "def main(data_map, experiment_result):\n" + \
        "\tdata_map['Data']['Collect'] = {}\n"

    aliases = {}

    for line in lines:
        if line.endswith("\n"):
            line = line[:-1]
        # Special commands
        if line.startswith("Test- "):
            config['name'] = line[6:]
        elif line.startswith("parameter "):
            di = line.find("(default ")
            if di == -1:
                param = line[10:]
                val = 0
                script += "\t" + param + " = data_map['Data']['Initial']['" + param + "']\n"
            else:
                param = line[10:di-1]
                val = line[di+9:-1]
                if val.startswith("\""):
                    val = val[1:-1]
                    script += "\t" + param + " = data_map['Data']['Initial']['" + param + "']\n"
                else:
                    val = float(val)
                    script += "\t" + param + " = float(data_map['Data']['Initial']['" + param + "'])\n"
            config['data'][param] = val
        elif line.find(" as ") > -1:
            ai = line.find(" as ")
            device = line[0:ai]
            alias = line[ai+4:]
            config['devices'].append(device)
            script += "\t" + alias + " = data_map['Devices']['" + device + "']\n"
            aliases[device] = alias
        else:
            # Replacements
            ret = line
            for device in config['devices']:
                dev = aliases[device]
                ind = 0
                while ret.find(dev + ";", ind) > -1:
                    ind = ret.find(dev + ";")
                    nxt = ret[ind+len(dev)+1:]
                    for fc in functions:
                        if nxt.startswith(fc[0]):
                            args = []
                            vs = nxt[len(fc[0]):].split(" ")
                            cont_index = 0
                            i = 0
                            while len(args) < fc[1] and i < len(vs):
                                if len(vs[i]) > 0:
                                    args.append(vs[i])
                                    cont_index += len(vs[i]) + 1
                                i += 1
                            func_call = "." + fc[2] + "("
                            delim = ""
                            for a in args:
                                func_call += delim + a
                                delim = ", "
                            func_call += ")"
                            ret = ret[:ind+len(dev)] + func_call + ret[ind+len(dev)+1+len(fc[0])+cont_index:]
                            ind = 0
                            break
                    else:
                        ind += 1

            ret = ret.replace("start timer", "start_time = time.time()")
            ret = ret.replace("get timer", "(time.time() - start_time)")
            if ret.strip("\t").startswith("print "):
                i = ret.find("print ")+6
                res = ret[:i]
                in_q = False
                in_p = False
                while i < len(ret):
                    c = ret[i]
                    if not in_q and not in_p:
                        if c not in '" +' and ret[i-1] == ' ':
                            in_p = True
                            res += "str("
                    if in_p and c in ' +':
                        res += ")"
                        in_p = False
                    if c == '"':
                        in_q = not in_q
                    res += c
                    i += 1
                if in_p:
                    res += ")"
                ret = res
            if ret.strip("\t").startswith("store "):
                i = ret.find("store ") + 6
                args = ret[i:].split(",")
                ret = args[1].strip() + " = " + ret[:i-6] + "data_map['Data']['Collect'][str(" + args[0].strip() + ")]"

            script += "\t" + ret + "\n"
    return config, script


def parse_input(lines):
    ret = []
    indent_count = 0
    imports = []
    for line in lines:
        iden = line[0]
        rv = ""
        for i in range(0, indent_count):
            rv += "\t"
        if iden == "IF":
            if line[2] == "/=":
                line[2] = "!="
            rv += "if " + line[1] + " " + line[2] + " " + line[3] + ":"
            indent_count += 1
        elif iden == "ELSE":
            # Unindent by one for the else but keep indentation count the same
            rv = rv[:-1]
            rv += "else:"
        elif iden == "END":
            # Unindent but don't print anything
            indent_count -= 1
            continue
        elif iden == "LOOP WHILE":
            rv += "while " + line[1] + " " + line[2] + " " + line[3] + ":"
            indent_count += 1
        elif iden == "PARAMETER":
            rv += "parameter " + line[1]
            if line[2] != "":
                rv += " (default " + line[2] + ")"
        elif iden == "SET":
            rv += line[1] + " = " + line[3]
        elif iden == "PRINT":
            rv += "print " + line[1]
        elif iden == "IMPORT":
            rv += line[1] + " as " + line[3]
        elif iden == "SAVE":
            rv += "store " + line[1] + "," + line[3]
        elif iden == "START TIMER":
            rv += "start timer"
        elif iden == "GET TIMER AS":
            rv += line[1] + " = get timer"
        elif iden == "FROM":
            if line[1] not in imports:
                imports.append(line[1])
            if line[2] == "CALL":
                rv += line[1].replace(" ", "_") + ";" + line[3] + " " + line[4]
            elif line[2] == "READ":
                rv += line[6] + " = " + line[1].replace(" ", "_") + ";" + line[3] + " " + line[4]
        rv = rv.replace(" ???", "")
        ret.append(rv)
    for dev in imports:
        ret.insert(0, dev + " as " + dev.replace(" ", "_"))
    return ret
