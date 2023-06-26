import React, { useState } from 'react';
import { TablaSimbolos } from './TabSimbolos';
import { Errores } from './Errores';
import './Reportes.css';
import { ArbolAST } from './ArbolAST';

export function Reportes() {
    const [estadoRep, setEstadoRep] = useState({ simbolos: '', errores: '', ast: ''});
    const [mostrarSimb, setMostrarSimb] = useState(false);
    const [mostrarErr, setMostrarErr] = useState(false);
    const [mostrarAST, setMostrarAST] = useState(false);

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
                setMostrarErr(false);
                setMostrarAST(false);
            });
    }

    const getErrores = () => {
        fetch('http://localhost:3000/errores', {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' },
            })
            .then(async (resp) => {
                let i = 1;
                const jsonRespuesta = await resp.json();
                const jsonModificado = jsonRespuesta.errores;
                if (jsonModificado != null){
                    jsonModificado.forEach(element => {
                        element['numero'] = i;
                        i++;
                    });
                }
                // console.log(jsonRespuesta);
                setEstadoRep({ ...estadoRep, errores: jsonModificado });
                setMostrarErr(true);
                setMostrarSimb(false);
                setMostrarAST(false);
            });
    }

    const getAST = () => {
        fetch('http://localhost:3000/ast', {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' },
            })
            .then(async (resp) => {
                let i = 1;
                const jsonRespuesta = await resp.json();
                const jsonModificado = jsonRespuesta.ast;
                // if (jsonModificado != null){
                //     jsonModificado.forEach(element => {
                //         element['numero'] = i;
                //         i++;
                //     });
                // }
                // console.log(jsonRespuesta);
                setEstadoRep({ ...estadoRep, ast: jsonModificado });
                setMostrarErr(false);
                setMostrarSimb(false);
                setMostrarAST(true);
            });
    }

    return(
        <div className="container-fluid">
            <div>
                <h1 className='titulo'>Reportes</h1>
            </div>
            <div className='centro'>
                <button className='btn btn-outline-success btn-lg m-2' onClick={() => getTablaSimbolos()}>Tabla de Símbolos</button>
                <button className='btn btn-outline-info btn-lg m-2' onClick={() => getErrores()}>Tabla de Errores</button>
                <button className='btn btn-outline-warning btn-lg m-2' onClick={() => getAST()}>Árbol de Análisis Sintáctico</button>
            </div>
            <div className='centro'>
                {(mostrarSimb) ? <TablaSimbolos rep = {estadoRep.simbolos}/> : null}
                {(mostrarErr) ? <Errores rep = {estadoRep.errores}/> : null}
                {(mostrarAST) ? <ArbolAST rep = {estadoRep.ast}/> : null}
            </div>
        </div>
    )
}