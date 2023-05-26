import sys
from Engine import Engine


def main():
    if (len(sys.argv) <= 2):
        print("Invalid input")
        return
    else:
        method = sys.argv[1]
        file_name = sys.argv[2]
        agent = Engine()
        agent.set_method(method)
        agent.knowledge_base.read_input_file(file_name)
        agent.do_algorithm()

main()