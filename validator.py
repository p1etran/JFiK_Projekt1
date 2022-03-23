# Piotr Augustyniak 299304
# Projekt 1 JFIK
from scanner import *
from parserPiotr import *
import re

def remove_comments(src):
    return re.sub('[\s*]+#.*', ' ', src) 

input_string = '''
begin
    j_in = voltagesource()
    r1 = resistor(1e3)
    c1 = capacitor(47e-9)
    d1 = diode(is=1e-15) # parametry diody są podawane przy pomocy nazwanych parametrów
    d2 = diode(is=1.8e-15, eta=2) # parametrów może być więcej niż jeden, albo zero (wtedy zakładane są domyślne wartości elementu)
    j_out = voltageprobe() # sonda napięcia nie posiada żadnych parametrów

    j_in[2] -- r1[1]
    j_in[1] -- gnd
    r1[2] -- c1[1] -- d1[2] -- d2[1] -- j_out[2]
    gnd -- c1[2] -- d1[1] -- d2[2] -- j_out[1]
end
'''


print(remove_comments(input_string))
scanner = Scanner(remove_comments(input_string))
#print(scanner.tokens)

parser = parser(scanner)
parser.start()
  
