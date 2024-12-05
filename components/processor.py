class Processor:
    LOAD = 0      # 000
    STORE = 1     # 001
    ADD = 2       # 010
    JUMP_IF = 3   # 011
    JUMP = 4      # 100
    HALT = 5      # 101
    LOAD_SIZE = 6 # 110
    INC = 7       # 111

    def __init__(self, memory):
        self.reg = [0] * 4  # 4 регистров общего назначения
        self.pc = 0  # Счетчик команд (Program Counter)
        self.memory = memory  # Память

    def execute_program(self):
        running = True
        while running:
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
            print(f"Загрузка в R{op1} значение {self.memory.data_memory[self.reg[2]]}")
        elif cmd_type == self.STORE:
            print(f"Значение из R{op2} ({self.reg[op2]}) записано в ячейку памяти {op1}.")
            self.memory.data_memory[op1] = self.reg[op2] 
        elif cmd_type == self.ADD:
            print(f"Сложение R{op2}({self.reg[op2]}) + R{op1}({self.reg[op1]}).")
            self.reg[op1] += self.reg[op2]  # Сложение данных двух регистров
        elif cmd_type == self.HALT:
            print("Остановка программы")
            return False
        elif cmd_type == self.JUMP:
            print(f"Переход")
            self.pc = op1 - 1  # Переход к указанному адресу
        elif cmd_type == self.JUMP_IF:
            print(f"Проверка условия совпадения {self.reg[2]} и {self.reg[3]}")
            if self.reg[2] == self.reg[3]:
                print(f"PC: {self.pc}")
                print("Регистры: " + ", ".join(map(str, self.reg)))
                print("Память данных: " + ", ".join(map(str, self.memory.data_memory)))
                self.pc = op1-1  # Переход к метке завершения
                return True # Не увеличивать PC, т.к. прыжок
        elif cmd_type == self.INC:
            if op1 < len(self.reg):
                self.reg[op1] += 1  # Увеличение значения регистра на 1
                print(f"Увеличен регистр R{op1} до {self.reg[op1]}")
            else:
                print("Ошибка: Индекс выходит за пределы при INC.")
        elif cmd_type == self.LOAD_SIZE:
            if op1 < len(self.reg):
                self.reg[op1] = self.memory.data_memory[0] + 1  # Автоматически загружаем размер массива в регистр
                print(f"Загружен размер массива: {self.reg[op1]} в R{op1}")
            else:
                print("Ошибка: Индекс выходит за пределы регистров при LOAD_SIZE.")
        else:
            print(f"Неизвестная команда: {cmd_type}")

        # Вывод текущего состояния процессора
        print(f"PC: {self.pc}")
        print("Регистры: " + ", ".join(map(str, self.reg)))
        print("Память данных: " + ", ".join(map(str, self.memory.data_memory)))

        return True
