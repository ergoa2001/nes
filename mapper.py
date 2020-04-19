class mapper:
	class mapper_000:
		def __init__(self, prgBanks, chrBanks):
			self.prgBanks = prgBanks
			self.chrBanks = chrBanks

		def cpuMapRead(self, addr):
			if addr >= 0x8000  and addr <= 0xFFFF:
				if self.prgBanks > 1:
					self.mapped_addr = addr & 0x7FFF
				else:
					self.mapped_addr = addr & 0x3FFF
				return True, self.mapped_addr
			return False, addr
		def cpuMapWrite(self, addr):
			if addr >= 0x8000  and addr <= 0xFFFF:
				return True, addr
			return False, addr
		def ppuMapRead(self, addr):
			if addr >= 0  and addr <= 0x1FFF:
				self.mapped_addr = addr
				return True, self.mapped_addr
			return False, addr
		def ppuMapWrite(self, addr):
			return False, addr
