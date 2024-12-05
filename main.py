from components.memory import Memory
from components.processor import Processor

class Program:
    @staticmethod
    def main():
        # Создание памяти
        memory = Memory(data_size=20)

        # Инициализация данных в памяти
        initial_data = [16, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 10, 10, 11]
        memory.load_data(initial_data)

        # Загрузка программы
        program = [
            0b000_0001_0000,  # LOAD R0, dmem[1] (Загрузить первый элемент в R0)
            0b111_0010_0000,  # INC R2 (Инициализировать счётчик позиций R2 на 1)
            0b110_0011_0000,  # LOAD_SIZE R3 (Загрузить размер массива в R3)

            # Метка начала цикла
            0b000_0001_0010,  # LOAD R1, dmem[R2] (Загрузить текущий элемент массива в R1)
            0b010_0000_0001,  # ADD R0, R1 (Добавить элемент к сумме)
            0b111_0010_0000,  # INC R2 (Увеличить счётчик позиций R2 на 1)

            # Проверка завершения цикла
            0b011_0010_0111,  # JUMP_IF R2 == R3 (Если R2 == R3, переход к завершению)
            0b100_0010_0000,  # JUMP START (Переход к началу цикла для следующего элемента)

            # Метка завершения программы
            0b001_1000_0000,  # STORE R0, dmem[9] (Сохранить сумму в dmem[9])
            0b101_0000_0000   # HALT (Завершить выполнение программы)
        ]
        memory.load_program(program)

        # Создание процессора и выполнение программы
        processor = Processor(memory)
        processor.execute_program()



if __name__ == "__main__":
    Program.main()
