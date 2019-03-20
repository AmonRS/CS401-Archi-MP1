import re

asm_file = open('test.asm', 'r')
hex_file = open('hex.dat', 'w')

opcodes = {
    'add':'11' , 'sub':'12' , 'mul':'13' , 'div':'14' , 'mod':'15', 'and':'16' , 'or':'17',
    'ld':'21' , 'st':'22' , 'li':'23',
    'jmp':'31',
    'mov':'41'
}
registers = {
    '%r0':'00','%r1':'01','%r2':'02','%r3':'03','%r4':'04','%r5':'05'
}



# INITIALIZE
part_of_code = 0
labels = {}
mem_adr = 0

# PARSE , read line by line
for line in asm_file:
    hexcode = ''

    # strip away whitespaces and newlines
    line = line.strip()

    # ignore comments and empty lines
    if line == '': continue
    if line[0:2] == '//': continue
    if '//' in line: line = line[:line.index('//')].strip()

    # .data section or .code section ?
    if line == '.data':
        part_of_code = 1
        continue
    elif line == '.code':
        part_of_code = 2
        continue

    print(mem_adr,'-',end='') # debug

    # data segment
    if part_of_code==1:
        labels[line[0:line.index(':')]] = [ hex(mem_adr)[2:] , [i for i in line[line.index(':')+1:].split(' ') if i != ''] ]
        mem_adr += 4 * len(labels[line[0:line.index(':')]][1])

    # code segment
    if part_of_code==2:
        l = [ i for i in re.split(' |,', line) if i != '' ]

        # check for labels
        for i in range(min(len(l),4)):
            if l[i] in labels:
                l[i] = labels[l[i]][0]


        # add opcode
        hexcode += opcodes[l[0]]
     
        # type of instruction ?
        if hexcode[0] == '1':
            # arithmetic op :     + - * / %
            hexcode = hexcode + registers[l[1]] + registers[l[2]] + registers[l[3]]     # op.rr.rr.rr
        elif hexcode[0] == '2':
            # data control :    load, store, and load_imm
            hexcode = hexcode + registers[l[1]] + hex(int(l[2]))[2:].zfill(4)       # op.rr.iiii
        elif hexcode[0] == '3':
            # jump
            hexcode = hexcode + hex(int(l[1]))[2:].zfill(6)        # jp.iiiiii
        elif hexcode[0] == '4':
            # mov
            hexcode = hexcode + registers[l[1]] + '00' + registers[l[2]]      # mv.r2.--.r1
        
        hex_file.write(hexcode+'\n')
        mem_adr += 4

    # debug
    print(part_of_code,'-', line,'-',hexcode)
print('labels: ', labels)

asm_file.close()
hex_file.close()