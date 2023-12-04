# x80Hao Assembler
# Andrew Schomber & Matthew Bernardon
# I pledge my honor that I have abided by the Stevens Honor System.

import os

# Dictionary of opcodes
opcodes = {
    "A": "00",
    "M": "01",
    "L": "10",
    "S": "11"
}

def clean():
    """Removes the object file and the ram file"""
    try:
        os.remove("instructions.o")
        os.remove("ram.o")
        print("Removed old object file and ram file.")
    except FileNotFoundError:
        pass

def read_file(file_name):
    """Reads in the file and returns a list of lines"""
    try:
        with open(file_name, "r") as f:
            lines = f.readlines()
            return lines
    except FileNotFoundError:
        print("File not found")
        exit()

def parse_line(line):
    """Parses the line and returns the opcode and register"""
    line = line.strip()
    line = line.split(" ")
    opcode = line[0]
    dst_register = line[1]
    rn_mem = line[2]
    rt = line[3] if opcode != "L" and opcode != "S" else 0
    return opcode, dst_register, rn_mem, rt


def assemble_line(opcode, dst_register, rn_mem, rt):
    """Assemble the line and return the machine code"""
    opcode = opcodes[opcode]
    dst_register = bin(int(dst_register))[2:].zfill(2)
    if opcode == "10" or opcode == "11":
        rn_mem = bin(int(rn_mem))[2:].zfill(4)
        # return hex opcode + dst_register + rn_mem
        return hex(int(opcode + dst_register + rn_mem, 2))[2:].zfill(2)

    else:
        rn_mem = bin(int(rn_mem))[2:].zfill(2)
    rt = bin(int(rt))[2:].zfill(2)
    
    return hex(int(opcode + dst_register + rn_mem + rt, 2))[2:].zfill(2)

def assemble(lines):
    """Assemble the lines and return the machine code"""
    machine_code = []
    for line in lines:
        opcode, dst_register, rn_mem, rt = parse_line(line)
        machine_code.append(assemble_line(opcode, dst_register, rn_mem, rt))
    return machine_code


def write_object_file(file_name, machine_code):
    """Create the object file and write the machine code to it"""
    object_file = "instructions.o"
    with open(object_file, "w") as f:
        f.write("v3.0 hex words addressed")
        for i in range(len(machine_code)):
            if i % 6 == 0:
                f.write("\n")
                f.write(hex(i)[2:].zfill(2) + ": ")
            f.write(machine_code[i] + " ")
        f.write("\n")

def generate_ram(line):
    """The first line of the assembly file is the decimal to be converted to hex to be loaded into RAM"""
    ram_file = "ram.o"
    with open(ram_file, "w") as f:
        f.write("v3.0 hex words addressed")
        for i in range(len(line)):
            if i % 6 == 0:
                f.write("\n")
                f.write(hex(i)[2:].zfill(2) + ": ")
            f.write(hex(int(line[i]))[2:].zfill(2) + " ")
        f.write("\n")
        

if __name__ == "__main__":
    clean()
    import sys
    if len(sys.argv) != 2:
        print("Usage: python3 as.py <file_name>")
        exit()
    file_name = sys.argv[1]
    lines = read_file(file_name)
    ram_line = lines[0].strip().split(" ")
    lines = lines[1:]
    machine_code = assemble(lines)
    write_object_file(file_name, machine_code)
    generate_ram(ram_line)
    print("Done!")