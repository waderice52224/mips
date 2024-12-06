import re
def main():
    # Defining the assembly file to read from
    filename = "textfiles/countdown.asm"

    # Read all lines from the assembly file, and store them in a list
    with open(filename, "r") as infile:
        lines = infile.readlines()

    # Step 1: Preprocess the lines to remove comments and whitespace
    # lines = preprocess_lines(lines)
    for i in lines:
        index = i.find("#")
        if index != -1:
            lines[lines.index(i)] = i[:index]
            i = i[:index]
        lines[lines.index(i)] = i.strip()
    lines = [line for line in lines if line != '']
    # Step 2: Use the preprocessed program to build data table
    data_table = build_data_table(lines)
    data_list = build_data_list(lines)
    lines = data_section_removed(lines)



    # Step 3: Build a label table and strip out the labels from the code
    # label_table, lines = create_label_table(lines)
    label_table = create_label_table(lines)
    # Step 4: Encode the program into a list of binary strings
    # encoded_program = encode_program(lines, label_table, data_table)
    for i in lines:
        print(encode_instruction(lines.index(i), i, label_table, data_table))



    # Step 5: Convert the strings to hexadecimal and write them to a file
    # hex_program = post_process(encoded_program)
    # with open("output.hex", "w") as outfile:
    #     outfile.write("v3.0 hex words addressed\n00: ")
    #     outfile.writelines(hex_program)

    # Step 6: Convert the data list to hexadecimal and write it to a file
    # with open("data.hex", "w") as outfile:
    #     outfile.write("v3.0 hex words addressed\n00: ")
    #     outfile.writelines([f"{d:04x} " for d in data_list])

def build_data_table(lines):
    for i in lines:
        if i.find(".text") != -1:
            run = True
            break
        else:
            run = False
    i = 0
    j = 0
    data_table = {}
    if run:
        while lines[i] != ".text":
            index = lines[i].find(":") + 1
            if index != 0:
                key = lines[i][:index].replace(":", "")
                value = j
                data_table[key] = value
                j += 1

            i += 1
        return data_table
    else:
        return {}


def build_data_list(lines):
    for i in lines:
        if i.find(".text") != -1:
            run = True
            break
        else:
            run = False
    i = 0
    data_list = []
    if run:
        while lines[i] != ".text":
            index = lines[i].find(":") + 1
            if index != 0:
                num = lines[i][index:]
                num = num.strip()
                num = int(num)
                data_list.append(num)
            i = i + 1
        return data_list
    else:
        return []


def data_section_removed(lines):
    for i in lines:
        if i.find(".text") != -1:
            run = True
            break
        else:
            run = False
    i = 0
    if run:
        while (lines[i] != ".text"):
            lines.remove(lines[i])
        lines.remove(lines[i])
        return lines
    else:
        return lines

def create_label_table(lines):
    i = 0
    value = 0
    label_table = {}
    for j in range(len(lines)):
        index = lines[i].find(":") + 1
        if lines[i].find(":") != -1:
            key = lines[i][:index].replace(":", "")
            label_table[key] = value
            lines.remove(lines[i])
        else:
            value += 1
            i += 1
    return label_table

def encode_instruction(line_num, instruction, label_table, data_table):
    instr_array = re.split(r'[,\s]+', instruction)
    instr = instr_array[0]

    match instr:
        case "add":
            final = addFunc(instr_array)
        case "sub":
            final = subFunc(instr_array)
        case "and":
            final = andFunc(instr_array)
        case "or":
            final = orFunc(instr_array)
        case "slt":
            final = sltFunc(instr_array)
        case "addi":
            final = addiFunc(instr_array)
        case "beq":
            final = beqFunc(instr_array, label_table)
        case "bne":
            final = bneFunc(instr_array, label_table, line_num)
        case "lw":
            final = lwFunc(instr_array, data_table)
        case "sw":
            final = swFunc(instr_array, data_table)
        case "j":
            final = jFunc(instr_array, label_table)
        case "jr":
            final = jrFunc(instr_array)
        case "jal":
            final = jalFunc(instr_array, label_table)
        case _:
            final = print("Unknown instruction")
    return final

def addFunc(instr_array):
    opcode = "0000"
    rs = int("".join(c for c in instr_array[2] if c.isdigit()))
    rs_bin = format(rs, '03b')
    rt = int("".join(c for c in instr_array[3] if c.isdigit()))
    rt_bin = format(rt, '03b')
    rd = int("".join(c for c in instr_array[1] if c.isdigit()))
    rd_bin = format(rd, '03b')
    funct = "010"
    final = str(opcode) + " " + rs_bin + " " + rt_bin + " " + rd_bin + " " + funct
    return final
def subFunc(instr_line):
    opcode = "0000"
    rs = int("".join(c for c in instr_line[2] if c.isdigit()))
    rs_bin = format(rs, '03b')
    rt = int("".join(c for c in instr_line[3] if c.isdigit()))
    rt_bin = format(rt, '03b')
    rd = int("".join(c for c in instr_line[1] if c.isdigit()))
    rd_bin = format(rd, '03b')
    funct = "110"
    final = str(opcode) + " " + rs_bin + " " + rt_bin + " " + rd_bin + " " + funct
    return final



def andFunc(instr_line):
    opcode = "0000"
    rs = int("".join(c for c in instr_line[2] if c.isdigit()))
    rs_bin = format(rs, '03b')
    rt = int("".join(c for c in instr_line[3] if c.isdigit()))
    rt_bin = format(rt, '03b')
    rd = int("".join(c for c in instr_line[1] if c.isdigit()))
    rd_bin = format(rd, '03b')
    funct = "000"
    final = str(opcode) + " " + rs_bin + " " + rt_bin + " " + rd_bin + " " + funct
    return final

def orFunc(instr_line):
    opcode = "0000"
    rs = int("".join(c for c in instr_line[2] if c.isdigit()))
    rs_bin = format(rs, '03b')
    rt = int("".join(c for c in instr_line[3] if c.isdigit()))
    rt_bin = format(rt, '03b')
    rd = int("".join(c for c in instr_line[1] if c.isdigit()))
    rd_bin = format(rd, '03b')
    funct = "001"
    final = str(opcode) + " " + rs_bin + " " + rt_bin + " " + rd_bin + " " + funct
    return final

def sltFunc(instr_line):
    opcode = "0000"
    rs = int("".join(c for c in instr_line[2] if c.isdigit()))
    rs_bin = format(rs, '03b')
    rt = int("".join(c for c in instr_line[3] if c.isdigit()))
    rt_bin = format(rt, '03b')
    rd = int("".join(c for c in instr_line[1] if c.isdigit()))
    rd_bin = format(rd, '03b')
    funct = "111"
    final = str(opcode) + " " + rs_bin + " " + rt_bin + " " + rd_bin + " " + funct
    return final



def addiFunc(instr_array):
    opcode = "0101"
    rs = int("".join(c for c in instr_array[1] if c.isdigit()))
    rs = format(rs, '03b')
    rt = int("".join(c for c in instr_array[2] if c.isdigit()))
    rt = format(rt, '03b')
    target = int(instr_array[3])
    target = format(target, '06b')
    final = str(opcode) + " " + str(rt) + " " + str(rs) + " " + target
    return final




def beqFunc(instr_array, label_table):
    opcode = "0011"
    rs = int("".join(c for c in instr_array[2] if c.isdigit()))
    rs_bin = format(rs, '03b')
    rt = int("".join(c for c in instr_array[1] if c.isdigit()))
    rt_bin = format(rt, '03b')
    label = instr_array[3]
    target_address = label_table[label]
    target_address_bin = format(target_address, '06b')
    final = str(opcode) + " " + rs_bin + " " + rt_bin + " " + target_address_bin
    return final


def bneFunc(instr_line, label_table, line_num):
    opcode = "0110"
    rt = int("".join(c for c in instr_line[1] if c.isdigit()))
    rt_bin = format(rt, '03b')
    rs = int("".join(c for c in instr_line[2] if c.isdigit()))
    rs_bin = format(rs, '03b')
    label = instr_line[3]
    label_address = label_table[label]
    offset = label_address - line_num - 1
    offset_bin = format(offset & 0x3F, '06b')
    final = str(opcode) + " " + rs_bin + " " + rt_bin + " " + offset_bin
    return final


def lwFunc(instr_line, data_table):
    opcode = "0001"
    rt = int("".join(c for c in instr_line[1] if c.isdigit()))
    rt_bin = format(rt, '03b')
    offset, base_reg = instr_line[2].replace(")", "").split("(")
    if not offset.strip().isdigit():
        label = offset.strip()
        offset_value = data_table.get(label, 0)
    else:
        offset_value = int(offset.strip())
    offset_bin = format(offset_value, '06b')
    rs = int("".join(c for c in base_reg.strip() if c.isdigit()))
    rs_bin = format(rs, '03b')
    final = str(opcode) + " " + rs_bin + " " + rt_bin + " " + offset_bin
    return final


def swFunc(instr_line, data_table):
    opcode = "0010"
    rt = int("".join(c for c in instr_line[1] if c.isdigit()))
    rt_bin = format(rt, '03b')
    offset, base_reg = instr_line[2].replace(")", "").split("(")
    if not offset.strip().isdigit():
        label = offset.strip()
        offset_value = data_table.get(label, 0)  # Get the label's address or default to 0 if not found
    else:
        offset_value = int(offset.strip())
    offset_bin = format(offset_value & 0x3F, '06b')  # Ensure it's within 6 bits
    rs = int("".join(c for c in base_reg.strip() if c.isdigit()))
    rs_bin = format(rs, '03b')
    final = str(opcode) + " " + rs_bin + " " + rt_bin + " " + offset_bin
    return final


def jFunc(instr_array, label_table):
    opcode = "0100"
    label = instr_array[1]
    target_address = label_table[label]
    target_address_bin = format(target_address, '012b')
    final = str(opcode) + " " + target_address_bin
    return final


def jrFunc(instr_line):
    # Opcode for jr is '000000' (6 bits, R-type instruction)
    opcode = "0111"

    # Extract the register number for rs (e.g., R5 or R7)
    rs = int("".join(c for c in instr_line[1] if c.isdigit()))  # Register (e.g., R5 or R7)
    rs_bin = format(rs, '03b')  # Convert rs to 5-bit binary

    # rt, rd, shamt are not used in jr, so these are always zero
    rt_bin = "000"
    rd_bin = "000"


    # The funct field for jr is '001000' (6 bits)
    funct_bin = "000"

    # Final instruction
    final = str(opcode) + " " + rs_bin + " " + rt_bin + " " + rd_bin + " " + funct_bin

    return final


def jalFunc(instr_line, label_table):
    opcode = "1000"
    label = instr_line[1]
    label_address = label_table[label]
    target_address = label_address
    target_address_bin = format(target_address, '012b')
    final = str(opcode) + " " + target_address_bin
    return final


main()