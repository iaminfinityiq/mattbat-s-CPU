from json import load

with open("program-settings.json") as settings_file:
    settings = load(settings_file)
    REGISTER_SIZE = settings["register-size"]
    REGISTERS = settings["memory-size"]
    INSTRUCTIONS = settings["instruction-size"]

class ALU:
    def __init__(self, inp1, inp2):
        self.inp1 = inp1[abs(len(inp1) - REGISTER_SIZE)::]
        if len(inp1) < REGISTER_SIZE:
            self.inp1 = "0" * (REGISTER_SIZE - len(inp1)) + inp1

        self.inp2 = inp2[abs(len(inp2) - REGISTER_SIZE)::]
        if len(inp2) < REGISTER_SIZE:
            self.inp2 = "0" * (REGISTER_SIZE - len(inp2)) + inp2

    def bitwise_and(self):
        out = ""
        for i in range(REGISTER_SIZE):
            out += str(int(self.inp1[i]) & int(self.inp2[i]))

        return out
    
    def bitwise_or(self):
        out = ""
        for i in range(REGISTER_SIZE):
            out += str(int(self.inp1[i]) | int(self.inp2[i]))

        return out
    
    def bitwise_xor(self):
        out = ""
        for i in range(REGISTER_SIZE):
            out += str((int(self.inp1[i]) | int(self.inp2[i])) & (~(int(self.inp1[i]) & int(self.inp2[i]))))

        return out
    
    def bitwise_nor(self):
        out = ""
        for i in range(REGISTER_SIZE):
            out += str(1 - (int(self.inp1[i]) | int(self.inp2[i])))

        return out
    
    def bitwise_xnor(self):
        out = ""
        for i in range(REGISTER_SIZE):
            out += str(1 - ((int(self.inp1[i]) | int(self.inp2[i])) & (~(int(self.inp1[i]) & int(self.inp2[i])))))

        return out
    
    def bitwise_nand(self):
        out = ""
        for i in range(REGISTER_SIZE):
            out += str(1 - (int(self.inp1[i]) & int(self.inp2[i])))

        return out
    
    def add(self):
        def half_adder(inp1, inp2):
            dummy = ALU(inp1, inp2)
            return {"carry": dummy.bitwise_and()[-1], "result": dummy.bitwise_xor()[-1]}
        
        def full_adder(inp1, inp2, carry):
            dummy1 = ALU(inp1, inp2)
            dummy2 = ALU(dummy1.bitwise_xor(), carry)
            result = dummy2.bitwise_xor()[-1]

            dummy3 = ALU(dummy1.bitwise_or(), carry)
            case1 = dummy3.bitwise_and()
            case2 = dummy1.bitwise_and()
            carry = ALU(case1, case2)
            carry = carry.bitwise_or()[-1]

            return {"carry": carry, "result": result}
        
        output = half_adder(self.inp1[-1], self.inp2[-1])
        result = output["result"]
        carry = output["carry"]
        for i in range(REGISTER_SIZE - 2, -1, -1):
            output = full_adder(self.inp1[i], self.inp2[i], carry)
            result = f"{output["result"]}{result}"
            carry = output["carry"]

        return result
    
    def subtract(self):        
        def invert(inp):
            result = ""
            for i in range(REGISTER_SIZE - 1):
                result += str(1 - int(inp[i]))

            return result + inp[-1]
        
        inp2 = invert(self.inp2)
        dummy = ALU(self.inp1, inp2)
        return dummy.add()
    
    def left_shift(self):
        dummy = ALU(self.inp2, self.inp2)
        return dummy.add()
    
    def right_shift(self):
        return self.inp2[1::]
