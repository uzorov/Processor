from components.instruction import Instruction

class Memory:
    def __init__(self, data_size):
        self.data_memory = [0] * data_size  # Инициализация массива данных
        self.command_memory = []  # Инициализация списка команд

    def load_data(self, initial_data):
        # Копирование начальных данных в память
        self.data_memory[:len(initial_data)] = initial_data

    def load_program(self, program):
        # Загрузка программы в память
        self.command_memory = program

    def fetch_instruction(self, pc):
        # Извлечение инструкции по адресу программы
        binary_instruction = self.command_memory[pc]
        instruction = Instruction(binary_instruction)
        print(f"Извлечена команда: {instruction}")
        return instruction

