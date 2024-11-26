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
        lines[lines.index(i)] = i[:index]
        i = i[:index]
        lines[lines.index(i)] = i.strip()
    for i in lines:
        if lines[lines.index(i)] == '':
            lines.remove(i)
    for i in lines:
        if lines[lines.index(i)] == '':
            lines.remove(i)

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
        encode_instruction(lines.index(i), i, label_table, data_table)



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
    print(line_num, end="| ")
    print(instruction, end="| ")
    print(label_table, end="| ")
    print(data_table, end="| ")
    print()
    instr_array = instruction.split()
    instr = instr_array[0]

    match instr:
        case "add":
            addFunc()
        case "sub":
            subFunc()
        case "and":
            andFunc()
        case "or":
            orFunc()
        case "slt":
            sltFunc()
        case "addi":
            addiFunc(instr_array)
        case "beq":
            beqFunc()
        case "bne":
            bneFunc()
        case "lw":
            lwFunc()
        case "sw":
            swFunc()
        case "j":
            jFunc()
        case "jr":
            jrFunc()
        case "jal":
            jalFunc()
        case _:
            print("Unknown instruction")


def addFunc():
    print("Executing add")


def subFunc():
    print("Executing sub")


def andFunc():
    print("Executing and")


def orFunc():
    print("Executing or")


def sltFunc():
    print("Executing slt")


def addiFunc(instr_array):
    print(instr_array)
    opcode = "0101"
    target_reg = "000"



def beqFunc():
    print("Executing beq")


def bneFunc():
    print("Executing bne")


def lwFunc():
    print("Executing lw")


def swFunc():
    print("Executing sw")


def jFunc():
    print("Executing j")


def jrFunc():
    print("Executing jr")


def jalFunc():
    print("Executing jal")


main()