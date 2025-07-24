# implementation by Freyja Wilkins of the brainfuck programming language created by Urban Muller
# reference specification avialable at esolangs.org/wiki/brainfuck
# text based adventure game written by Truttle1 available at https://pastebin.com/1E5US36E
# source file is read according to first console argument
from sys import argv as args
FIRST_CELL, LAST_CELL, CELL_COUNT = 0, 29999, 30000
MAX_VALUE, MIN_VALUE = 255, 0
class Reader:
# emulates the behavior of the C function getc() of which many non-trivial brainfuck programs rely on
    def __init__(self) -> None:
        self.data : str = ""
    def read(self) -> chr:
        if not len(self.data):
            self.data = input() + "\n"
        return_value : chr = self.data[0]
        self.data = self.data[1:]
        return return_value
class Stack:
    def __init__(self, max_depth : int = 200) -> None:
        self.data : list[int] = []
        self.max_depth = max_depth
    def push(self, push_value : int) -> None:
        if len(self.data) == self.max_depth:
            return error_handler(1)
        self.data.append(push_value)
    def pop(self) -> int:
        if not len(self.data):
            error_handler(2)
            return 0
        return self.data.pop()
    def peek(self) -> int:
        return_value = self.pop()
        self.push(return_value)
        return return_value
def retrieve_source() -> str:
    with open(args[1], "rt") as source_file: return source_file.read()
def interpreter(code : str) -> None:
    code_length : int = len(code)
    code_pointer : int = 0
    error_state : int | None = None
    flow_stack : Stack = Stack()
    cell : list[int] = [MIN_VALUE for _ in range(CELL_COUNT)]
    cell_pointer : int = FIRST_CELL
    reader : Reader = Reader()
    def error_handler(error_code : int) -> None:
        error_message : tuple[str] = [
            "unknown error", #error 0
            "stack overflow", #error 1
            "stack underflow", #error 2
            "no corresponding closing loop", #error 3
        ]
        print(f"Error {error_code}: {error_message[error_code]}")
        error_state = error_code
    def skip_loop() -> None:
        nonlocal code_pointer
        nests : int = 0
        while code_pointer < code_length:
            if code[code_pointer] == "[":
                nests += 1
            elif code[code_pointer] == "]":
                nests -= 1
                if nests == 0:
                    return
            code_pointer += 1
        return error_handler(3)
    def begin_loop() -> None:
        if cell[cell_pointer] == MIN_VALUE:
            return skip_loop()
        flow_stack.push(code_pointer)
    def end_loop() -> None:
        nonlocal code_pointer
        if cell[cell_pointer] == MIN_VALUE: flow_stack.pop()
        else: code_pointer = flow_stack.peek()
    while error_state == None and code_pointer < code_length:
        match code[code_pointer]:
            case "+": cell[cell_pointer] = MIN_VALUE if cell[cell_pointer] == MAX_VALUE else cell[cell_pointer] + 1
            case "-": cell[cell_pointer] = MAX_VALUE if cell[cell_pointer] == MIN_VALUE else cell[cell_pointer] - 1
            case "<": cell_pointer = LAST_CELL if cell_pointer == FIRST_CELL else cell_pointer - 1
            case ">": cell_pointer = FIRST_CELL if cell_pointer == LAST_CELL else cell_pointer + 1
            case ".": print(chr(cell[cell_pointer]), end = "")
            case ",": cell[cell_pointer] = ord(reader.read()) & MAX_VALUE
            case "[": begin_loop()
            case "]": end_loop()
        code_pointer += 1
def main():
    interpreter(retrieve_source())
if __name__ == "__main__":
    main()
