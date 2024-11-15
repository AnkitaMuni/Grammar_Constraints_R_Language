from r_parser import parse
import sys

def parse_file(filename):
    with open(filename, 'r') as f:
        data = f.read()
    return parse(data)

if __name__ == '__main__':
    try:
        result = parse_file('input.txt')
        print("Input syntax is correct")
        print("Parse result:")
        print(result)
    except SyntaxError as e:
        print("Input syntax is incorrect")
        print(f"Error: {str(e)}")
        sys.exit(1)

# execute this file in terminal