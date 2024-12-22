class Processor:
    LOAD = 0      # 000
    STORE = 1     # 001
    ADD = 2       # 010
    JUMP_IF = 3   # 011
    JUMP = 4      # 100
    HALT = 5      # 101
    CMP = 6 # 110
    INC = 7       # 111

    def __init__(self, memory):
        self.reg = [0] * 4  # 4 регистров общего назначения
        self.pc = 0  # Счетчик команд (Program Counter)
        self.memory = memory  # Память
        self.cmp_flag = 0  # Начальное значение флага сравнения


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
            self.reg[op1] = self.memory.data_memory[self.reg[op2]]  # Загрузка данных из памяти в регистр
            print(f"Загрузка в R{op1} значение {self.memory.data_memory[self.reg[op2]]}")
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
            print(f"Проверка совпадения чисел (используется CMP флаг)")
            if self.cmp_flag == 0:
                print(f"PC: {self.pc}")
                print("Регистры: " + ", ".join(map(str, self.reg)))
                print("Память данных: " + ", ".join(map(str, self.memory.data_memory)))
                print(f"Первый операнд: {op1}")
                print(f"Второй операнд: {op2}")
                self.pc = op1-1  # Переход к метке завершения
                return True # Не увеличивать PC, т.к. прыжок
        elif cmd_type == self.INC:
            if op1 < len(self.reg):
                self.reg[op1] += 1  # Увеличение значения регистра на 1
                print(f"Увеличен регистр R{op1} до {self.reg[op1]}")
            else:
                print("Ошибка: Индекс выходит за пределы при INC.")
        elif cmd_type == self.CMP:
            if op1 < len(self.reg) and op2 < len(self.reg):
                if self.reg[op1] > self.reg[op2]:
                    self.cmp_flag = 1  # Первый регистр больше второго
                elif self.reg[op1] < self.reg[op2]:
                    self.cmp_flag = -1  # Первый регистр меньше второго
                else:
                    self.cmp_flag = 0  # Регистр равны
                print(f"Сравнение R{op1}({self.reg[op1]}) и R{op2}({self.reg[op2]}). Флаг: {self.cmp_flag}")
            else:
                print("Ошибка: Индекс выходит за пределы при CMP.")


        # Вывод текущего состояния процессора
        print(f"PC: {self.pc}")
        print("Регистры: " + ", ".join(map(str, self.reg)))
        print("Память данных: " + ", ".join(map(str, self.memory.data_memory)))

        return True
