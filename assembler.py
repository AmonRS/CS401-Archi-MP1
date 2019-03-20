import re

asm_file = open('test.asm', 'r')
hex_file = open('hex.dat', 'w')

opcodes = {
    'add':'11' , 'sub':'12' , 'mul':'13' , 'div':'14' , 'mod':'15',
    'ld':'21' , 'st':'22' , 'li':'23' , 'mov':'24',
    'br':'31' , 'beq':'33'
}
registers = {
    '%r0':'00'
}



# init
part_of_code = 0
labels = {}

# read line by line
for line in asm_file:
    hexcode = ''

    # strip away whitespaces and newlines
    line = line.strip()

    # ignore comments and empty lines
    if line == '': continue
    if line[0:2] == '//': continue

    if line == '.data':
        part_of_code = 1
        continue
    elif line == '.code':
        part_of_code = 2
        continue

    # data segment
    if part_of_code==1:
        labels[line[0:line.index(':')]] = [i for i in line[line.index(':')+1:].split(' ') if i != '']

    # code segment
    if part_of_code==2:
        l = [ i for i in re.split(' |,', line) if i != '' ]
        # add opcode
        hexcode += opcodes[l[0]]
        # type of instruction ?
        pass


    print(part_of_code,'-', line)

    
print('labels: ', labels)



