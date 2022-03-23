# Piotr Augustyniak 299304
# Projekt 1 JFIK

import collections
import re

Token = collections.namedtuple('Token', ['type', 'value', 'line', 'column'])

class Scanner:

  def __init__(self, input):
    self.tokens = []
    self.current_token_number = 0
    for token in self.tokenize(input):
        self.tokens.append(token)
 
  def tokenize(self, input_string):
    keywords = {'voltagesource', 'voltageprobe', 'currentsource', 'currentprobe', 'resistor', 'capacitor', 'inductor', 'diode', 'gnd', 'begin' , 'end'}
    token_specification = [
	('SCNUMBER', r'[\+\-]?[0-9]+(\.[0-9]+)?e[\+\-]?[0-9]+'), # Scientific notation
        ('NUMBER',  r'\d+(\.\d*)?'), # Integer or decimal number
        ('CHAINID',  r'[a-zA-Z0-9_]+\[[1-2]\]'), # Integer or decimal number
        ('EQ',  r'='),               # Equality operator
        ('CONNECTION',  r'--'),               # Equality operator
        ('END',     r';'),           # Statement terminator
        ('ID',      r'[a-zA-Z0-9_]+'),   # Identifiers
#        ('OP',      r'[+*\/\-]'),    # Arithmetic operators
        ('NEWLINEE', r'[\n]{2,}'),          # Line endings
        ('NEWLINE', r'\n'),          # Line endings
        ('SKIP',    r'[ \t]'),       # Skip over spaces and tabs
	('COMMA',   r','),           # Comma
        ('OB',     r'\('),           # Open normal bracket
        ('CB',     r'\)'),           # Close normal bracket
        ('OSB',     r'\['),          # Open square bracket
        ('CSB',     r'\]'),          # Close square bracket
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    get_token = re.compile(tok_regex).match
    line_number = 1
    current_position = line_start = 0
    match = get_token(input_string)
    while match is not None:
        type = match.lastgroup
        if type == 'NEWLINE':
            line_start = current_position
            line_number += 1
        elif type != 'SKIP':
            value = match.group(type)
            if type == 'ID' and value in keywords:
                type = value
            yield Token(type, value, line_number, match.start()-line_start)
        current_position = match.end()
        match = get_token(input_string, current_position)
    if current_position != len(input_string):
        raise RuntimeError('Error: Unexpected character %r on line %d' % \
                              (input_string[current_position], line_number))
    yield Token('EOF', '', line_number, current_position-line_start)

  def next_token(self):
    self.current_token_number += 1
    if self.current_token_number-1 < len(self.tokens):
      return self.tokens[self.current_token_number-1]
    else:
      raise RuntimeError('Error: No more tokens')

