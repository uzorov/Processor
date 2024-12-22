from components.memory import Memory
from components.processor import Processor
from components.assembler import Assembler

class Program:
    @staticmethod
    def main():
        # Считывание программы из файла
        with open("test.txt", "r", encoding='utf-8') as f:
            program_text = f.readlines()

        # Создание ассемблера
        assembler = Assembler()

        # Преобразование текста программы в машинный код
        machine_code = assembler.assemble(program_text)

        # Инициализация памяти
        memory = Memory(6)  

        initial_data = [6, 10, 0, 1, 30, 40, 0]
        memory.load_data(initial_data)

        # Загрузка программы в память
        memory.load_program(machine_code)

        # Создание процессора и выполнение программы
        processor = Processor(memory)
        processor.execute_program()


if __name__ == "__main__":
    Program.main()
