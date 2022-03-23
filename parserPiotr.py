# Piotr Augustyniak 299304
# Projekt 1 JFIK
class parser:

  ##### Parser header #####
  def __init__(self, scanner):
    self.next_token = scanner.next_token
    self.token = self.next_token()

  def take_token(self, token_type):
    if self.token.type != token_type:
      self.error("Unexpected token: %s" % token_type)
    if token_type != 'EOF':
      self.token = self.next_token()

  def error(self,msg):
    raise RuntimeError('Parser error, %s' % msg)

  ##### Parser body #####

  # Starting symbol
  def start(self):
    # start -> BEGIN program END
    if self.token.type == 'begin':
      print('begin ok')
      self.take_token('begin')
      self.program()
    else:
      self.error('no begin at start')
    if self.token.type == 'end':
      self.take_token('end')
      print('end ok')
    else:
      self.error('no end')

  def program(self):
    # program -> commands NEWLINEE chain
    if self.token.type == 'ID':
      self.commands()
      self.program()
    if self.token.type == 'NEWLINEE':
       print('linia odstepu ok')
       self.take_token('NEWLINEE')
       if self.token.type == 'CHAINID':
          print('chain ok')
          self.chain()
          self.program()
       else:
          self.error('wrong chainid')

  def commands(self):
    # commands -> command commands
    if self.token.type == 'ID':
      self.command()
      self.commands()

  def command(self):
    # command -> ID EQ element 
    if self.token.type == 'ID':
      self.take_token('ID')
    if self.token.type == 'EQ':
      self.take_token('EQ')
      self.element()
    else:
      self.error('no eq in command')


  def element(self):
    # element -> sourcesvalue 
    #         -> probesvalue 
    #         -> electricelementsvalue
    #         -> diodesvalue 
    if self.token.type == 'voltagesource' or self.token.type == 'currentsource':
      self.sourcesvalue()
    elif self.token.type == 'voltageprobe' or self.token.type == 'currentprobe':
      self.probesvalue()
    elif self.token.type == 'resistor' or self.token.type == 'inductor' or self.token.type == 'capacitor':
      self.electricelementsvalue()
    elif self.token.type == 'diode':
      self.diodesvalue()
    else:
      self.error('wrong element name')

  def sourcesvalue(self):
    # sourcesvalue -> VOLTAGESOURCE|CURRENTSOURCE ( eps )
    #	           -> VOLTAGESOURCE|CURRENTSOURCE ( NUMBER ) 
    if self.token.type == 'voltagesource':
      self.take_token('voltagesource')
    if self.token.type == 'currentsource':
      self.take_token('currentsource')
    if self.token.type == 'OB':
      self.take_token('OB')
    if self.token.type == 'NUMBER':
      self.take_token('NUMBER')
      self.take_token('CB')
      print('sourcesvalue ok')
    elif self.token.type == 'CB':
      self.take_token('CB')
      print('sourcesvalue ok')
    else:
      self.error('wrong sourcesvalue')

  def probesvalue(self):
    # probesvalue -> VOLTAGEPROBE|CURRENTPROBE ( eps )
    if self.token.type == 'voltageprobe':
      self.take_token('voltageprobe')
    if self.token.type == 'currentprobe':
      self.take_token('currentprobe')
    if self.token.type == 'OB':
      self.take_token('OB')
    else:
      self.error('no open bracket in probesvalue')
    if self.token.type == 'CB':
      self.take_token('CB')
      print('probesvalue ok')
    else:
      self.error('wrong value in probesvalue')

  def electricelementsvalue(self):
    # electricelementsvalue -> RESISTOR|CAPACITOR|INDUCTOR ( NUMBER )
    #	                    -> RESISTOR|CAPACITOR|INDUCTOR ( SCNUMBER )
    if self.token.type == 'resistor':
      self.take_token('resistor')
    elif self.token.type == 'capacitor':
      self.take_token('capacitor')
    elif self.token.type == 'inductor':
      self.take_token('inductor')
    if self.token.type == 'OB':
      self.take_token('OB')
    else:
      self.error('no open bracket in electricelemtsvalue')
    if self.token.type == 'SCNUMBER':
      self.take_token('SCNUMBER')
      if self.token.type == 'CB':
         self.take_token('CB')
         print('electricelemntsvalue ok')
      else:
         self.error('no closing bracket in electricelemtsvalue')
    elif self.token.type == 'NUMBER':
      self.take_token('NUMBER')
      if self.token.type == 'CB':
         self.take_token('CB')
         print('electricelemntsvalue ok')
      else:
         self.error('no closing bracket in electricelemtsvalue')
    if self.token.type == 'CB':
      self.error('wrong value in electricelemtsvalue')
 
  def diodesvalue(self):
    # diodesvalue -> DIODE ( eps )
    #             -> DIODE ( diodeparameters )
    self.take_token('diode')
    if self.token.type == 'OB':
      self.take_token('OB')
    else:
      self.error('no open bracket in diode')  
    if self.token.type == 'CB':
      self.take_token('CB')
      print('diode ok')
    if self.token.type == 'ID':
      self.diodeparameters()
    else:
      self.error('wrong value in diode')

  def diodeparameters(self):
    # diodeparameters -> diodeparameter diodeparameter_next
    self.diodeparameter()
    self.diodeparameter_next()
 

  def diodeparameter(self):
    # diodeparameter -> ID EQ NUMBER
    #                -> ID EQ SCNUMBER 
    self.take_token('ID')
    self.take_token('EQ')
    if self.token.type == 'NUMBER':
      self.take_token('NUMBER')
    elif self.token.type == 'SCNUMBER':
      self.take_token('SCNUMBER')
    if self.token.type == 'CB':
      self.take_token('CB')


  def diodeparameter_next(self):
    # diodeparameter_next -> eps
    #	                  -> COMMA diodeparameter diodeparameter_next
    if self.token.type == 'COMMA':
      self.take_token('COMMA')
      self.diodeparameter()
      self.diodeparameter_next()
    if self.token.type == 'CB':
      self.take_token('CB')
    else:
      pass

  def chain(self):
    # chain -> CHAINID chain_next
    #       -> gnd chain_next
    if self.token.type == 'CHAINID':
      self.take_token('CHAINID')
      self.chain_next()
    elif self.token.type == 'gnd':
      self.take_token('gnd')
      self.chain_next()

  def chain_next(self):
    # chain_next -> CONNECTION chain
    if self.token.type == 'CONNECTION':
      self.take_token('CONNECTION')
      self.chain()
      self.chain_next()
    else:
      self.chain()


