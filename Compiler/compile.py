import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from instructions import *
import struct

class GUI:
    def __init__(self):
        #
        # INIT GUI
        #
        self.root = tk.Tk()
        self.root.title("MIPSIM Compiler")

        # output_textbox - output for program messages and other peer messages
        self.output_textbox = tk.Text(self.root, height=10, width=50)
        self.output_textbox.grid(row=1, column=0, padx=0, pady=0)

        # compile - button to compile the file
        self.connect = ttk.Button(self.root, text="Compile", command=self.compile)
        self.connect.grid(row=2, column=0, padx=5, pady=5)

        self.label = tk.Label(self.root, text="Click to choose a text file to compile", width=40, height=10, bg="lightgrey")
        self.label.grid(row=0, column=0, padx=0, pady=0)

        self.label.bind("<ButtonRelease-1>", self.drop)

        self.root.mainloop()

        self.CONTENT_LOAD = b''

    # Handle Drag And Drop files
    def drop(self, event):
        self.file_path = filedialog.askopenfilename()
        if not self.file_path:
            return
        
        print(self.file_path)

        basenameIndex = 0
        pathLength = len(self.file_path)
        for i in range(pathLength):
            if(self.file_path[i] == '/'):
                basenameIndex = i+1

        self.label.config(text="Click to choose a text file to compile\n"+self.file_path[basenameIndex:pathLength])


    def compile(self):
        compilation_success = True

        # Loading the content of the file
        self.CONTENT_LOAD = b''
        compiled_lines = []
        immediate_lines = []
        # Open the file in binary mode
        with open(self.file_path, 'r') as file:

            # Extracting each individual line and processing it
            lines = file.readlines()
            line_index=0
            for line in lines:
                line_index += 1
                hex_index, immediate, length = getInstruction(line)
                if(hex_index == -1):
                    self.output_textbox.insert(tk.END, f"Error on line {line_index}: Invalid instruction" + '\n')
                    compilation_success = False
                    continue

                # Extracting Information, position of each value
                value_positions, last_separator = getValuePositions(line)
                if(len(value_positions) > 3):
                    self.output_textbox.insert(tk.END, f"Error on line {line_index}: Too many register prefixes ($)" + '\n')
                    compilation_success = False
                if(immediate):
                    #value_positions.append(last_separator)
                    if(abs(value_positions[len(value_positions)-1]-last_separator) < 2):
                        self.output_textbox.insert(tk.END, f"Error on line {line_index}: Invalid immediate instruction" + '\n')
                        compilation_success = False
                    else:
                        value_positions.append(last_separator)

                if(len(value_positions) < 2 and hex_index != 0x0):
                    self.output_textbox.insert(tk.END, f"Error on line {line_index}: Too few arguments" + '\n')
                    compilation_success = False

                # Extracting Values out of value positions
                values = getValues(line, value_positions, immediate)
                values.insert(0, hex_index)

                #print("Extracted values:")
                #for i in range(len(values)):
                #    if(values[i] == -1):
                #        self.output_textbox.insert(tk.END, f"Error on line {line_index}: Invalid values or registers" + '\n')
                #    print(values[i])


                compiled_line = 0
                if(immediate):
                    compiled_line = pack_values_im(values)
                else:
                    compiled_line = pack_values(values)
                compiled_lines.append(compiled_line)
                immediate_lines.append(immediate)

                print(f"compiled line: {compiled_line:#010x}")
                #print(f"inversed line: {inversePackedVals(compiled_line):#010x}")
            print(f"Number of instructions: {len(compiled_lines)}")

        if(compilation_success == False):
            self.output_textbox.insert(tk.END, f"Compilation Failed" + '\n')
            return
        
        with open("compiled.mp", 'wb') as file:
            # Adding Instruction Count
            instructionCount = len(compiled_lines)
            binary_data = struct.pack('I', instructionCount)
            file.write(binary_data)

            # Adding Compiled Lines
            for i in range(len(compiled_lines)):
                if(immediate_lines[i] == False):
                    binary_data = struct.pack('I', inversePackedVals(compiled_lines[i]))
                else:
                    binary_data = struct.pack('I', compiled_lines[i])
                file.write(binary_data)

            # Adding end of the file
            # Here should be Label handling
            file_EOF = 0
            binary_data = struct.pack('I', file_EOF)
            file.write(binary_data)
            file_EOF = 4
            binary_data = struct.pack('I', file_EOF)
            file.write(binary_data)
            file_EOF = 0
            binary_data = struct.pack('I', file_EOF)
            file.write(binary_data)
            file_EOF = 9
            binary_data = struct.pack('I', file_EOF)
            file.write(binary_data)
            


def inversePackedVals(val):
    val_bytes = val.to_bytes(4, byteorder='big')
    val_bytes = val_bytes[::-1]
    return int.from_bytes(val_bytes, byteorder='big')

# returns instruction binary code and next value index, if it returns -1, instruction is invalid
def getInstruction(line):
    length = 4
    instruction = line[:length]
    for _ in range(2):
        if(instruction[length-1] == ' ' or instruction[length-1] == '$' or instruction[length-1] == '\n' or instruction[length-1] == '#'):
            length -= 1
            instruction = line[:length]

    print(instruction)

    hex_index = -1
    immediate = False
    if(instruction in instructionSet):
        hex_index, immediate = instructionSet[instruction]()

    #if(immediate):
    #    print(f"hex: {hex_index}, immediate: True, length: {length}")
    #else:
    #    print(f"hex: {hex_index}, immediate: False, length: {length}")

    return hex_index, immediate, length

def getValuePositions(line):
    # Extracting Information, position of each value
    register_positions = []
    last_separator = 0
    for i in range(len(line)):
        if(line[i] == "$"):
            register_positions.append(i)
        elif(line[i] == ","):
            last_separator = i
        elif(line[i] == "#"):
            break
    #print(f"last sep {last_separator+1}")
    return register_positions, last_separator+1

def getValues(line, value_positions, immediate):
    #for i in range(len(value_positions)):
    #    print(f"val pos: {value_positions[i]}")

    values = []
    # Iterating through each value
    iterate = len(value_positions)
    if(immediate):
        iterate -= 1
    for i in range(iterate):
        length = 0
        for j in range(value_positions[i]+1, min(value_positions[i]+3, len(line))):
            if(isNumber(line[j])):
                length += 1
            else:
                break
        value = ""
        if(length == 0):
            values.append(-1)
        else:
            for j in range(length):
                value = value + line[value_positions[i]+1+j]

            try:
                values.append(int(value))
            except:
                values.append(-1)

    if(immediate):
        length = 0
        for j in range(value_positions[iterate], min(value_positions[iterate]+4, len(line))):
            #print(f"checking number {line[j]}")
            if(isNumberHex(line[j])):
                length += 1
            else:
                break
        value = ""
        if(length == 0):
            #print("bad len")
            values.append(-1)
            
        else:
            for j in range(length):
                value = value + line[value_positions[iterate]+j]
            try:
                values.append(int(value, 16))
            except:
                #print("exception")
                values.append(-1)

    return values

def pack_values_im(values):
    formatted_vals = [0,0,0,0]
    for i in range(len(values)-1):
        formatted_vals[i] = values[i]
    
    formatted_vals[3] = values[len(values)-1]
    
    # Ensure values are within 5 bits (0-31)
    assert 0 <= formatted_vals[0] < 256
    assert 0 <= formatted_vals[1] < 32
    assert 0 <= formatted_vals[2] < 32
    assert 0 <= formatted_vals[3] < 65536

    # Shift each value to the correct position
    packed_value = ((formatted_vals[0] & 0xFF) << 24) | ((formatted_vals[2] & 0x1F) << 21) | ((formatted_vals[1] & 0x1F) << 16) | (formatted_vals[3] & 0xFFFF)
    
    # The packed value is now a 32-bit integer
    return packed_value

def pack_values(values):
    formatted_vals = [0,0,0,0]
    # Ensure values are within 5 bits (0-31)
    for i in range(len(values)):
        formatted_vals[3-i] = values[i]
    assert 0 <= formatted_vals[0] < 32
    assert 0 <= formatted_vals[1] < 32
    assert 0 <= formatted_vals[2] < 32
    assert 0 <= formatted_vals[3] < 256

    # Shift each value to the correct position
    packed_value = ((formatted_vals[0] & 0x1F) << 21) | ((formatted_vals[1] & 0x1F) << 16) | ((formatted_vals[2] & 0x1F) << 11) | (formatted_vals[3] & 0xFF)

    # The packed value is now a 32-bit integer
    return packed_value


def isNumber(char):
    ascii = ord(char)
    if(ascii >= 48 and ascii <= 57):
        return True
    return False

def isNumberHex(char):
    ascii = ord(char)
    if((ascii >= 48 and ascii <= 57) or (ascii >= 65 and ascii <= 70) or (ascii >= 97 and ascii <= 102)):
        return True
    return False


            
instructionSet = {
    "ADD": function_add,
    "ADDI": function_addi,
    "AND": function_and,
    "ANDI": function_andi,
    "BEQ": function_beq,
    "BNEQ": function_bneq,
    "DIV": function_div,
    "DIVU": function_divu,
    "LI": function_li,
    "LUI": function_lui,
    "LW": function_lw,
    "MUL": function_mul,
    "MULU": function_mulu,
    "NOP": function_nop,
    "NOR": function_nor,
    "OR": function_or,
    "ORI": function_ori,
    "SLLV": function_sllv,
    "SRLV": function_srlv,
    "SUB": function_sub,
    "SUBI": function_subi,
    "SW": function_sw,
    "XOR": function_xor,
    "XORI": function_xori
}

def main():
    window = GUI()

if __name__ == "__main__":
    main()