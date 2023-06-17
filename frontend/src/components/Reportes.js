import { TablaSimbolos } from './TabSimbolos';
import './Reportes.css';

export function Reportes() {
    return(
        <div className="container-fluid">
            <div>
                <h1 className='titulo'>Reportes</h1>
            </div>
            <div className='centro'>
                <button className='btn btn-outline-success btn-lg m-2'>Tabla de Símbolos</button>
                <button className='btn btn-outline-info btn-lg m-2' >Tabla de Errores</button>
                <button className='btn btn-outline-warning btn-lg m-2' >Árbol de Análisis Sintáctico</button>
            </div>
            <div className='centro'>
                <TablaSimbolos/>
            </div>
        </div>
    )
}