from anytree import Node, RenderTree

# Example of valid inputs: ε, 01, 0101, 010011, 001101
# Example of invalid inputs: 0, 1, 011, 1001

class LL1Parser:
    def __init__(self, grammar_file):
        self.grammar = {}
        self.load_grammar(grammar_file)
        self.stack = []
        self.parse_tree_root = Node("S")  

    # Reads the grammar.txt file
    def load_grammar(self, filename):
        with open(filename, 'r') as file:
            for line in file:
                non_terminal, production = line.strip().split("->")
                self.grammar[non_terminal.strip()] = [p.strip() for p in production.split('|')]

    # Parsing method
    def parse(self, input_string):
        # Treat 'ε' input as an empty string
        if input_string == 'ε':
            input_string = ''

        self.stack = [(self.parse_tree_root, 'S')]  # Stack holds tuples of (node, grammar symbol)
        index = 0

        while self.stack:
            current_node, top = self.stack.pop()
            
            if top == 'ε':
                Node("ε", parent=current_node) 
                continue
            
            elif top == 'X':
                if index < len(input_string) and input_string[index] == '0':
                    # Match "0X1" production for X
                    node_0 = Node("0", parent=current_node)
                    node_X = Node("X", parent=current_node)
                    node_1 = Node("1", parent=current_node)
                    self.stack.append((node_1, '1'))
                    self.stack.append((node_X, 'X'))
                    self.stack.append((node_0, '0'))
                else:
                    # Use epsilon production for X
                    Node("ε", parent=current_node)

            elif top == 'S':
                # Match "XX" production for S
                left_X = Node("X", parent=current_node)
                right_X = Node("X", parent=current_node)
                self.stack.append((right_X, 'X'))
                self.stack.append((left_X, 'X'))

            elif index < len(input_string) and input_string[index] == top:
                index += 1  # Advance input pointer when top match with input
                
            else:
                print("Parse Error: Unmatched symbol at", index)
                return False

        if index == len(input_string):
            print("Parse Successful")
            return True
        else:
            print("Parse Error: Remaining unparsed input")
            return False

    # Display parse tree if input is valid
    def display_parse_tree(self):
        print("Parse Tree:")

        RED = "\033[91m"
        END_COLOR = "\033[0m"

        # Color the resulted string
        def colorize(node_name):
            if node_name in {'0', '1', 'ε'}:
                return f"{RED}{node_name}{END_COLOR}"
            return node_name

        for pre, fill, node in RenderTree(self.parse_tree_root):
            print(f"{pre}{colorize(node.name)}")

if __name__ == "__main__":
    print("————THIS IS A SIMPLE LL(1) PARSER————")
    grammar_file = input("Please, input the grammar file: ")

    parser = LL1Parser(grammar_file)
    print("Loaded grammar:", parser.grammar)
    
    input_string = input("Please, input the string: ")

    if parser.parse(input_string):
        parser.display_parse_tree()
    else:
        print("Error in parsing the input string.")
