class Processor:
    def __init__(self, memory):
        self.reg = [0] * 4  # 4 регистра общего назначения
        self.pc = 0  # Счетчик команд

        # Константы команд
        self.LOAD = 0      # 000
        self.STORE = 1     # 001
        self.ADD = 2       # 010
        self.JUMP_IF = 3   # 011
        self.JUMP = 4      # 100
        self.HALT = 5      # 101
        self.LOAD_SIZE = 6 # 110
        self.INC = 7       # 111

        self.memory = memory

    def execute_program(self):
        running = True
        while running:
            print(f"Итерация цикла: PC={self.pc}, R2={self.reg[2]}, R3={self.reg[3]}")
            instruction = self.memory.fetch_instruction(self.pc)  # Извлечение команды
            running = self.decode_and_execute(instruction)  # Декодирование и выполнение команды
            self.pc += 1  # Переход к следующей команде
            print()

    def decode_and_execute(self, instruction):
        cmd_type = instruction.cmd_type
        op1 = instruction.operand1
        op2 = instruction.operand2


        if cmd_type == self.LOAD:
            self.reg[op1] = self.memory.data_memory[self.reg[2]]  # Загрузка данных из памяти в регистр
            print(f"Загрузка в R{op1}: {self.reg[op1]} из памяти [{self.reg[2]}]")

        elif cmd_type == self.STORE:
            print(f"Значение из R{op2} ({self.reg[op2]}) записано в последний элемент памяти.")
            self.memory.data_memory[self.memory.data_memory[0] + 1] = self.reg[op2]  # Сохранение данных в память

        elif cmd_type == self.ADD:
            self.reg[op1] += self.reg[op2]  # Сложение данных двух регистров
            print(f"Сложение: R{op1} = {self.reg[op1]}")

        elif cmd_type == self.HALT:
            print("Остановка программы")
            return False

        elif cmd_type == self.JUMP:
            print(f"Переход на {op1}")
            self.pc = op1
            return True

        elif cmd_type == self.JUMP_IF:
            if op1 < len(self.reg):
                # Условный прыжок: если R2 == R3, перейти к завершению
                if self.reg[2] == self.reg[3]:  # Сравнение R2 и R3
                    self.pc = op2  # Переход к указанному адресу (корректируем PC на 1, чтобы избежать auto-increment)
                    print(f"Условный переход: PC -> {self.pc + 1}")
                    return True  # Прерываем выполнение текущей команды, чтобы не увеличивать PC
            else:
                print("Ошибка: Индекс выходит за пределы при JUMP_IF.")
                
        elif cmd_type == self.INC:
            if op1 < len(self.reg):
                self.reg[op1] += 1  # Увеличение значения регистра
                print(f"Увеличен регистр R{op1} до {self.reg[op1]}")
            else:
                print("Ошибка: Индекс выходит за пределы при INC.")

        elif cmd_type == self.LOAD_SIZE:
            if op1 < len(self.reg):
                self.reg[op1] = self.memory.data_memory[0] + 1  # Загрузка размера массива в регистр
                print(f"Загружен размер массива: {self.reg[op1]} в R{op1}")
            else:
                print("Ошибка: Индекс выходит за пределы регистров при LOAD_SIZE.")

        else:
            print(f"Неизвестная команда: {cmd_type}")

        # Вывод текущего состояния процессора
        print(f"PC: {self.pc}")
        print(f"Регистры: {self.reg}")
        print(f"Память данных: {self.memory.data_memory}")

        return True
