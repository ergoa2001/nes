from arbne.cpu import cpu as CPU


class BUS:
    def __init__(self):
        self.mem = bytearray(2**16)
        self.debugmode = True

    def cpuWrite(self, addr, data):
        self.mem[addr] = data

    def cpuRead(self, addr, readOnly=False):
        return self.mem[addr]


class ArbneCPUBridge:
    def start(self):
        self.cpu = CPU(BUS())
        self.cpu.reset()
        self.cpu.cycles = 0
        self.cycles = 0
        self.STACK_PAGE = 0x100

    def cpu_pc(self, counter):
        self.cpu.pc = counter

    def memory_set(self, pos, val):
        self.cpu.write(pos, val)

    def memory_fetch(self, pos):
        return self.cpu.read(pos)

    def execute(self):
        self.cpu.cycles = 0
        self.cpu.clock()
        return self.cpu.cycles, None

    def cpu_set_register(self, register, value):
        if register == 'P':
            self.cpu.flagC = [0, 1][0 != value & 1]   # Carry
            self.cpu.flagZ = [0, 1][0 != value & 2]   # Zero
            self.cpu.flagI = [0, 1][0 != value & 4]   # Disable interrupts
            self.cpu.flagD = [0, 1][0 != value & 8]   # Decimal mode
            self.cpu.flagB = [0, 1][0 != value & 16]  # Break
            self.cpu.flagU = [0, 1][0 != value & 32]  # Unused
            self.cpu.flagV = [0, 1][0 != value & 64]  # Overflow
            self.cpu.flagN = [0, 1][0 != value & 128]   # Negative
            self.cpu.status = value
        elif register == 'SP':
            self.cpu.stkp = value
        else:
            setattr(self.cpu, register.lower(), value)

    def cpu_register(self, register):
        if register == 'P':
            return self.cpu.status
        elif register == 'SP':
            return self.cpu.stkp
        return getattr(self.cpu, register.lower())

    def cpu_flag(self, flag):
        return bool(getattr(self.cpu, f'flag{flag}'))

    def cpu_set_flag(self, flag):
        setattr(self.cpu, f'flag{flag}', 1)

    def cpu_unset_flag(self, flag):
        setattr(self.cpu, f'flag{flag}', 0)

    def cpu_push_byte(self, byte):
        addr = self.STACK_PAGE + self.cpu.stkp
        self.cpu.write(addr, byte)
        self.cpu.stkp -= 1

    def cpu_pull_byte(self):
        addr = self.STACK_PAGE + self.cpu.stkp + 1
        val = self.cpu.read(addr)
        self.cpu.stkp += 1
        return val

    def cpu_push_word(self, word):
        hi, lo = divmod(word, 0x100)
        self.cpu_push_byte(hi)
        self.cpu_push_byte(lo)

    def cpu_pull_word(self):
        b1 = self.cpu_pull_byte()
        b2 = self.cpu_pull_byte() << 8
        return b1 + b2
