import os
import Sintactico as Analizar
from Sym.TablaSimbolos import TablaSimbolos

def main():
    env = TablaSimbolos()
    
    absolutepath = os.path.abspath(__file__)
    fileDirectory = os.path.dirname(absolutepath)
    f = open(os.path.join(fileDirectory, 'archivoPrueba.txt'), 'r')
    s = f.read()
    # s = '''
    #     // prueba comentario
    #     /* comentario
    #     multilinea
    #     */
    #     let a:string = "hola";
    #     let b = 50+10*5;
    #     let c:string = "mundo";
    #     console.log(a);
    #     console.log(b);
    #     console.log(a + c);
    #     '''
    ast = Analizar.parse(s)

    for inst in ast:
        inst.ejecutar(env)

main()