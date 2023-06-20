import React, { useState } from 'react';
import { TablaSimbolos } from './TabSimbolos';
import './Reportes.css';

export function Reportes() {
    const [estadoRep, setEstadoRep] = useState({ simbolos: '', errores: '', ast: ''});
    const [mostrarSimb, setMostrarSimb] = useState(false);

    const getTablaSimbolos = () => {
        fetch('http://localhost:3000/simbolos', {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' },
            })
            .then(async (resp) => {
                let i = 1;
                const jsonRespuesta = await resp.json();
                const jsonModificado = jsonRespuesta.simbolos;
                if (jsonModificado != null){
                    jsonModificado.forEach(element => {
                        element['numero'] = i;
                        i++;
                    });
                }
                // console.log(jsonRespuesta);
                setEstadoRep({ ...estadoRep, simbolos: jsonModificado });
                setMostrarSimb(true);
            });
    }

    return(
        <div className="container-fluid">
            <div>
                <h1 className='titulo'>Reportes</h1>
            </div>
            <div className='centro'>
                <button className='btn btn-outline-success btn-lg m-2' onClick={() => getTablaSimbolos()}>Tabla de Símbolos</button>
                <button className='btn btn-outline-info btn-lg m-2' >Tabla de Errores</button>
                <button className='btn btn-outline-warning btn-lg m-2' >Árbol de Análisis Sintáctico</button>
            </div>
            <div className='centro'>
                {(mostrarSimb) ? <TablaSimbolos rep = {estadoRep.simbolos}/> : null}
            </div>
        </div>
    )
}