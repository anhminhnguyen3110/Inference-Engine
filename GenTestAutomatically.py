import random
import subprocess
from termcolor import colored

def generate_horn_clause(num_symbols, number_of_horn_clauses=10):    
    symbols = [chr(i) for i in range(ord('a'), ord('a') + num_symbols)]
    
    horn_clauses = []
    for i in range(num_symbols*number_of_horn_clauses):
        consequent = random.choice(symbols)
        antecedents = random.sample(symbols, random.randint(1, num_symbols - 1))
        clause = f"{'&'.join(antecedents)}=>{consequent}"
        horn_clauses.append(clause)
    
    tell = '; '.join(horn_clauses)
    ask = random.choice(symbols)
    
    program = f'TELL\n{tell}\nASK\n{ask}\n'
    
    return program


METHODS = ["FC", "BC", "TT"]
program1_path_1 = "./dist/main.exe"
program1_path_2 = "./dist/other.exe"

def run_tests(num_tests, program1_path, program2_path, num_symbols_low=10, num_symbols_high=20, number_of_horn_clauses=10, horn_clause = True):
    for i in range(num_tests):
        if(horn_clause):
            program = generate_horn_clause(num_symbols=random.randint(num_symbols_low, num_symbols_high), number_of_horn_clauses=number_of_horn_clauses)
        for method in METHODS:
            input_test = "./dist/input.txt"
            with open(input_test, "w") as f:
                f.write(program)
                
            result1 = subprocess.run([program1_path, method, input_test], capture_output=True)
            output1 = result1.stdout.decode().strip()
            
            result2 = subprocess.run([program2_path, method, input_test], capture_output=True)
            output2 = result2.stdout.decode().strip()
            
            if output1 == output2:
                print(f"Test {i+1} with method {colored(method, 'yellow')}: {colored('PASS', 'green')}")
            else:
                print(f"Test {i+1} with method {colored(method, 'yellow')}: {colored('FAILED', 'red')}")
                failed_test = f"./dist/failed_test_{i+1}.txt"
                failed_test_out_put_my = f"./dist/failed_test_output_{i+1}_method_{method}_my.txt"
                failed_test_out_put_other = f"./dist/failed_test_output_{i+1}_method_{method}_other.txt"
                with open(failed_test, "w") as f:
                    f.write(program)
                with open(failed_test_out_put_my, "w") as f:
                    f.write(output1)
                with open(failed_test_out_put_other, "w") as f:
                    f.write(output2)
        


run_tests(10000, program1_path_1, program1_path_2, 2, 20, 2)
