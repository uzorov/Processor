from components.instruction import Instruction

class Memory:
    def __init__(self, data_size: int):
        # Инициализация памяти
        self.data_memory = [0] * data_size  # Память данных
        self.command_memory = []           # Память команд

    def load_data(self, initial_data: list[int]):
        # Загрузка начальных данных в память
        self.data_memory[:len(initial_data)] = initial_data

    def load_program(self, program: list[int]):
        # Загрузка программы (список команд)
        self.command_memory = program

    def fetch_instruction(self, pc: int):
        # Извлечение команды из памяти команд
        binary_instruction = self.command_memory[pc]
        instruction = Instruction(binary_instruction)
        print(f"Извлечена команда: {instruction}")
        return instruction
