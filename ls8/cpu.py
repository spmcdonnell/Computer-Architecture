"""CPU functionality."""

import sys


# LOAD
LDI = 0b10000010
# Print
PRN = 0b01000111
# Multiply
MUL = 0b10100010
# Halt
HTL = 0b00000001


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.pc = 0
        self.reg = [0] * 8

    def load(self):
        """Load a program into memory."""

        address = 0

        if len(sys.argv) != 2:
            print(f"Usage format: {sys.argv[0]} filename")
            sys.exit(1)

        try:
            with open(sys.argv[1]) as opened_file:
                for line in opened_file:

                    num = line.split('#', 1)[0]

                    self.ram[address] = int(num, 2)

                    address += 1

        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} was not found.")
            sys.exit(2)

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
            return self.reg[reg_a]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        PRN = 0b01000111
        LDI = 0b10000010
        MUL = 0b10100010
        HTL = 0b00000001

        while True:

            ir = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if ir == PRN:

                print(self.reg[operand_a])
                self.pc += 2

            elif ir == LDI:

                self.reg[operand_a] = operand_b
                self.pc += 3

            elif ir == MUL:

                self.alu('MUL', operand_a, operand_b)
                self.pc += 3

            elif ir == HTL:

                break
