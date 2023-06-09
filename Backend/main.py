

import Sintactico as Analizar

def main():
    s = '''
        console.log(5!== 8 && 8>=6);
        console.log(true || false);
        console.log(!true);'''
    ast = Analizar.parse(s)

    for inst in ast:
        inst.ejecutar(None)

main()