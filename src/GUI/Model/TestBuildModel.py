functions = [("set voltage", 1, "set_voltage"),
             ("set output switch", 1, "set_output_switch"),
             ("measure average", 0, "get_average")]


def parse_file(filename):
    """
    Parse a test description file and produce a JSON config and a Python script.
    :param filename: The file to be parsed.
    :return: A corresponding JSON config and Python script.
    """
    with open(filename) as f:
        config = dict()
        config['Devices'] = []
        config['Experiment'] = []
        config['Data'] = {}
        script = "import time\n" + \
            "def main(data_map, experiment_result):\n" + \
            "\tdata_map['Data']['Collect'] = {}\n"

        aliases = {}

        for line in f.readlines():
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


if __name__ == "__main__":
    config, script = parse_file("../../../VA.txt")
    print config
    print script
