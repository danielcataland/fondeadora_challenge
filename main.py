import re

def main_func():

    validate_quantity_format('(!)')
    in_operation = ''
    while(in_operation != '0'):
        in_operation = input('Select the operation you need:\n'+
        '1 - Encode string\n' +
        '2 - Decode string\n' +
        '0 - Exit program\n')
        selected_op = ''
        if in_operation == '1':
            selected_op = input('Insert string to encode: \n')
            return print(manage_operations(selected_op, 1))
        elif in_operation == '2':
            selected_op = input('Insert string to decode: \n')
            return print(manage_operations(selected_op, 2))
        elif not in_operation != '1' or not in_operation != '2' or in_operation != '0':
            print('Operation not supported')

def manage_operations(str_to_encode = str, op = int):
    if op == 1:
        valid, reason = validate_input_encode(str_to_encode)
        if not valid:
            return reason

        print('Your string was converted to uppercase for better encoding')
        return_str = encode_rle(str_to_encode.upper())
        if len(return_str) >= len(str_to_encode):
            return_str = 'No compression needed'
            return return_str
        return return_str
    else:
        valid, reason = validate_input_decode(str_to_encode)
        if not valid:
            return reason
        return_str = decode_rle(str_to_encode)
        return return_str

def validate_input_encode(in_str = str):

    if not in_str:
        return False, 'String not provided'

    if not in_str.isalpha():
        return False, 'String must contains only chars [A-Z]'
    return True, ''

def validate_input_decode(in_str = str):
    if not in_str:
        return False, 'String not provided'

    if in_str.count('(') != in_str.count(')'):
        return False, 'Incorrect input format, verify your input'

    all_occur = re.findall(r'\([a-z1-9]+\)$', in_str)

    if not in_str[0].isupper():
        return False, 'Incorrect input format, verify your input'

    if len(all_occur) == 0 and not in_str.isupper():
        return False, 'Incorrect input format, verify your input'

    for i in in_str: 
        if i.isnumeric() or i == '(' or i == ')' or i.islower():
            return False, 'Incorrect input format, verify your input'

    return True, ''

def validate_quantity_format(in_str = str):
    for idx, i in enumerate(in_str):
        if idx != 0 and i != ')':
            if i.isalpha() and i.islower():
                if i < in_str[idx + 1]:
                    return False
            else:
                if i.isnumeric():
                    if int(i) <= 2 and idx == 1:
                        return False
                    if i.isnumeric() and in_str[idx + 1] != ')':
                        return False
                else:
                    if i.isupper():
                        return False
                    if not i.isalnum():
                        return False
    return True

def encode_rle(str_enc = str):
    final_result = []
    main_counter = 1

    for i in range(1, len(str_enc)):
        if str_enc[i] == str_enc[i -1]:
            main_counter += 1
        else:
            if main_counter == 2:
                final_result.append(str_enc[i-1]*2)
                main_counter = 1
            else:
                if main_counter == 1:
                    final_result.append(str_enc[i-1])
                    main_counter = 1
                else:
                    if main_counter >= 10:
                        final_result.append(str_enc[i-1] + '(' + encode_ascii_rule(main_counter) + ')')
                        main_counter = 1
                    else:
                        final_result.append(str_enc[i-1] + '(' + str(main_counter) + ')')
                        main_counter = 1
    
    if main_counter == 2:
        final_result.append(str_enc[i-1]*2)
    else:
        if main_counter == 1:
            final_result.append(str_enc[-1])
        else:
            final_result.append(str_enc[-1] + '(' +  encode_ascii_rule(main_counter) + ')')

    return ''.join(final_result)

def encode_ascii_rule(ascii_num = int):
    final_str = []
    ascii_code = ascii_num + 87
    while ascii_code >= 123:
        final_str.append('z')
        ascii_code = ascii_code - 35
    if ascii_code >= 97:
        final_str.append(chr(ascii_code))
    else:
        final_str.append(str(ascii_code - 87))
    
    return ''.join(final_str)

def decode_ascii_rule(alphanum = str):
    total_counter = 0
    for i in alphanum:
        if i.isalpha():
            total_counter += (ord(i) - 87)
        else:
            total_counter += int(i)
    return total_counter

def decode_rle(decode_str = str):
    alpha_str = []
    residue = []
    counter = 1
    total_multiply = 0
    final_str = []
    for idx, i in enumerate(decode_str):
        if i == '(':
            j=''
            while j != ')':
                j=decode_str[idx+counter]
                if j == ')':
                    total_multiply = decode_ascii_rule(''.join(alpha_str))
                    if len(residue) > 0: 
                        residue.pop()
                    final_str.append(''.join(residue))
                    final_str.append(decode_str[idx - 1] * total_multiply)
                    counter = 1
                    alpha_str.clear()
                    residue.clear()
                    break
                else:
                    alpha_str.append(decode_str[idx+counter])
                    counter += 1
            counter = 1
        else:
            if i != ')' and not i.isnumeric() and i.isupper():
                residue.append(i)
            
    if len(residue) > 0:
        final_str.append(''.join(residue))
    return ''.join(final_str)

if __name__ == '__main__':
    main_func()
