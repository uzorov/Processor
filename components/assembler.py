class Assembler:
    def __init__(self):
        self.label_table = {}  # Таблица меток
        self.unresolved_labels = []  # Неразрешённые метки

    def assemble(self, instructions):
        machine_code = []
        command_index = 0

        # Первый проход: анализ меток и команд
        for line in instructions:
            trimmed_line = line.strip()
            
            #Игнорировать пустые строки и строки с комментариями
            if not trimmed_line or trimmed_line.startswith("#"):
                continue

            # Лексический анализ: распознавание меток
            if trimmed_line.endswith(":"):
                label = trimmed_line[:-1]
                if label in self.label_table:
                    raise ValueError(f"Метка {label} уже определена.")
                self.label_table[label] = command_index
                print(f"Метка {label} определена на строке {command_index}")
                continue
            
            command_part = trimmed_line.split("#")[0].strip()

            # Синтаксический анализ команды
            parts = command_part.split()
            cmd_type = parts[0].upper()

            if not self.is_valid_command(cmd_type):
                raise ValueError(f"Неизвестная команда: {cmd_type}")

            # Обработка операндов с метками
            operand1 = self.parse_operand(parts[1], command_index, 0) if len(parts) > 1 else 0
            operand2 = self.parse_operand(parts[2], command_index, 1) if len(parts) > 2 else 0
            print(f"Генерируем команду из cmdType={cmd_type}, operand1={operand1}, operand2={operand2}, command_index={command_index}")
            binary_instruction = self.generate_instruction(cmd_type, operand1, operand2)
            machine_code.append(binary_instruction)
            command_index += 1

        # Второй проход: разрешение меток
        self.resolve_labels(machine_code)

        return machine_code

    def is_valid_command(self, cmd_type):
        return cmd_type in ["LOAD", "STORE", "ADD", "JUMP_IF", "JUMP", "HALT", "CMP", "INC"]

    def generate_instruction(self, cmd_type, operand1, operand2):
        if cmd_type == "LOAD":
            binary_instruction = (0 << 8) | (operand1 << 4) | operand2
        elif cmd_type == "STORE":
            binary_instruction = (1 << 8) | (operand1 << 4) | operand2
        elif cmd_type == "ADD":
            binary_instruction = (2 << 8) | (operand1 << 4) | operand2
        elif cmd_type == "JUMP_IF":
            binary_instruction = (3 << 8) | (operand1 << 4) 
        elif cmd_type == "JUMP":
            binary_instruction = (4 << 8) | (operand1 << 4)
        elif cmd_type == "HALT":
            binary_instruction = (5 << 8)
        elif cmd_type == "CMP":
            binary_instruction = (6 << 8) | (operand1 << 4) | operand2
        elif cmd_type == "INC":
            binary_instruction = (7 << 8) | (operand1 << 4)
        else:
            raise ValueError(f"Неизвестная команда: {cmd_type}")

        print(f"Добавлена команда {cmd_type} ({bin(binary_instruction)[2:].zfill(11)})")
        return binary_instruction

    def parse_operand(self, operand, command_index, operand_index):
        # Если операнд является числом
        try:
            value = int(operand)
            return value
        except ValueError:
            pass

        # Если операнд является меткой
        if operand in self.label_table:
            resolved_address = self.label_table[operand]
            print(f"Метка {operand} разрешена, указывает на адрес {resolved_address}")
            return resolved_address

        # Если метка ещё не определена, добавляем в нерешённые метки
        self.unresolved_labels.append((operand, command_index, operand_index))
        print(f"Метка {operand} не разрешена, добавлена в нерешённые на строке {command_index} с индексом {operand_index}")
        return 0  # Временно

    def resolve_labels(self, machine_code):
        for unresolved in self.unresolved_labels:
            label, command_index, operand_index = unresolved

            if label not in self.label_table:
                raise ValueError(f"Неразрешённая метка: {label}")

            resolved_address = self.label_table[label]
            print(f"Разрешаем метку {label} на строке {command_index}, адрес: {resolved_address}")

            # Обновляем нужный операнд
            instruction = machine_code[command_index]
            if operand_index == 0:  # Для JUMP
                machine_code[command_index] = (instruction & 0xF0F) | (resolved_address << 4)
                print(f"Обновлён операнд на адрес {resolved_address}")
            elif operand_index == 1:  # Для JUMP_IF
                machine_code[command_index] = (instruction & 0xFF0) | resolved_address
                print(f"Обновлён операнд на адрес {resolved_address}")

