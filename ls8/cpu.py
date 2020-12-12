"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.registers = [0] * 8
        self.registers[7] = 0xF4
        self.pc = 0
        self.fl = 0b00000000

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        address = 0

        if len(sys.argv) < 2:
            print(f'Error from {sys.argv[0]}: missing file name')
            sys.exit(1)

        with open(sys.argv[1]) as f:
            for line in f:
                split_line = line.split("#")[0]
                stripped_split_line = split_line.strip()

                if stripped_split_line != "":
                    command = int(stripped_split_line, 2)
                    
                    # load command into memory
                    self.ram_write(address, command)

                    address += 1

        # for instruction in program:
        #     # self.ram[address] = int(instruction[0:8], 2)
        #     self.ram_write(address, instruction)
        #     address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.registers[reg_a] += self.registers[reg_b]
        elif op == "SUB": 
            self.registers[reg_a] -= self.registers[reg_b]
        elif op == "MUL":
            self.registers[reg_a] *= self.registers[reg_b]
        elif op == "CMP":
            self.fl = 0b00000000
            if self.registers[reg_a] == self.registers[reg_b]:
                self.fl = 0b00000001
            elif self.registers[reg_a] > self.registers[reg_b]:
                self.fl = 0b00000010
            elif self.registers[reg_a] < self.registers[reg_b]:
                self.fl = 0b00000100
        else:
            raise Exception("Unsupported ALU operation")        

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()
    
    def ram_read(self, idx):
        return self.ram[idx]

    def ram_write(self, idx, value):
        self.ram[idx] = value

    def run(self):
        """Run the CPU."""
        HLT = 0b00000001
        LDI = 0b10000010
        PRN = 0b01000111
        MUL = 0b10100010
        PUSH = 0b01000101
        POP = 0b01000110
        CMP = 0b10100111
        JMP = 0b01010100
        JEQ = 0b01010101
        JNE = 0b01010110


        SP = 7

        print('running')

        running = True
        
        while running:

            IR = self.ram_read(self.pc)
            
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if IR == HLT:
                running = False

            elif IR == LDI:
                self.registers[operand_a] = operand_b
                self.pc += 3

            elif IR == PRN:
                print(self.registers[operand_a])
                self.pc += 2

            elif IR == MUL:    
                self.registers[operand_b] *= self.registers[operand_b]
                self.pc += 3

            elif IR == PUSH:
                self.registers[SP] -= 1
                self.ram_write(self.registers[operand_a], self.registers[SP])
                self.pc += 2

            elif IR == POP:
                value = self.ram_read(self.registers[SP])
                self.registers[operand_a] = value
                self.registers[SP] += 1
                self.pc += 2

            elif IR == JMP:
                self.pc = self.registers[operand_a]
                return

            elif IR == JEQ:
                if self.FL == 0b00000001:
                    self.pc = self.registers[operand_a]
                    return

            elif IR == JNE:
                if not (self.fl & 0b001):
                    self.pc = self.registers[operand_a]
                    return
            
            else: 
                self.pc+=1
