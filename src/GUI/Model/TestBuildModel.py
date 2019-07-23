def parse_lines(lines, output_file, functions):
    """
    Parse a test description file and produce a JSON config and a Python script.
    :param lines: The lines to be parsed.
    :param output_file: The output file name.
    :param functions: The function names.
    :return: A corresponding JSON config and Python script.
    """
    config = dict()
    config['Name'] = output_file.replace("_", " ")
    config['Devices'] = []
    config['Experiment'] = [{
                  "Type": "PY_SCRIPT",
                  "Source": output_file + ".py",
                  "Order":  1
                },
                {
                    "Type": "PY_SCRIPT",
                    "Source": "CustomTestReduce.py",
                    "Order": 2
                }
    ]
    config['Data'] = {}
    script = "import time\n" + \
        "def main(data_map, experiment_result):\n" + \
        "\tdata_map['Data']['Collect'] = {}\n"

    aliases = {}

    for line in lines:
        if line.endswith("\n"):
            line = line[:-1]
        # Special commands
        if line.startswith("Test- "):
            config['Name'] = line[6:]
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
            config['Data'][param] = val
        elif line.find(" as ") > -1:
            ai = line.find(" as ")
            device = line[0:ai]
            alias = line[ai+4:]
            config['Devices'].append(device)
            script += "\t" + alias + " = data_map['Devices']['" + device + "']\n"
            aliases[device] = alias
        else:
            # Replacements
            ret = line
            for device in config['Devices']:
                dev = aliases[device]
                while ret.find(dev + ";") > -1:
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
                            break
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
                ret = res
            if ret.strip("\t").startswith("store "):
                i = ret.find("store ") + 6
                args = ret[i:].split(",")
                ret = ret[:i-6] + "data_map['Data']['Collect'][str(" + args[0].strip() + ")] = " + args[1].strip()

            script += "\t" + ret + "\n"
    return config, script


def parse_input(lines):
    ret = []
    indent_count = 0
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
            if line[2] == "CALL":
                rv += line[1] + ";" + line[3]
            elif line[2] == "READ":
                rv += line[5] + " = " + line[1] + ";" + line[3]
        rv = rv.replace(" ???", "")
        ret.append(rv)
    return ret
