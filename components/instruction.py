class Instruction:
    def __init__(self, binary_instruction: int):
        # Извлечение полей команды
        self.cmd_type = (binary_instruction >> 8) & 0x7  # Извлечение битов 9-8
        self.operand1 = (binary_instruction >> 4) & 0xF  # Извлечение битов 7-4
        self.operand2 = binary_instruction & 0xF         # Извлечение битов 3-0

    def __str__(self):
        # Возвращает строковое представление команды
        return (f"CmdType: {bin(self.cmd_type)[2:].zfill(3)}, "
                f"Operand1: {bin(self.operand1)[2:].zfill(4)}, "
                f"Operand2: {bin(self.operand2)[2:].zfill(4)}")
