import React, { useState } from 'react';
import CodeMirror from '@uiw/react-codemirror';
import { StreamLanguage } from '@codemirror/language';
import { go } from '@codemirror/legacy-modes/mode/go';
import { javascript } from '@codemirror/lang-javascript';
import { sublime, abcdef, xcodeDark } from '@uiw/codemirror-themes-all';

export function Editor(){
    const [estado, setEstado] = useState({ editor: '', consola: '', c3d: ''});

    const interpretarEntrada = () => {
        setEstado({...estado, consola: estado.consola + 'prueba\n'})
        console.log(estado);
    }

    return(
        <div className='container-fluid'>
            <div>
                <h1 style={ {textAlign: 'center'}}>Editor</h1>
            </div>
            <div>
                <button className='btn btn-outline-success btn-lg m-2' onClick={() => interpretarEntrada()}>Interpretar</button>
                <button className='btn btn-outline-info btn-lg m-2' >Compilar</button>
            </div>
            <br />
            <br />
            <div className="row">
                <div className="col-md-6">
                    <h3>Entrada</h3>
                    <br/>
                    <CodeMirror
                        value=""
                        height="500px"
                        theme={sublime}
                        extensions={[javascript({ typescript: true })]}
                        onChange={(value) => {
                            setEstado({ ...estado, editor: value});
                        }}
                    />
                    <br/>
                </div>
                <div className="col-md-6">
                    <h3>Consola</h3>
                    <br/>
                    <CodeMirror
                        value={estado.consola}
                        height="500px"
                        theme={abcdef}
                        extensions={[javascript({ typescript: true })]}
                        readOnly = {true}
                        // onChange={(value) => {
                        //     setEstado({ ...estado, consola: value});
                        // }}
                    />
                    <br/>
                </div>
            </div>
            <div className="row">
                <div className='col-md-3'></div>
                <div className="col-md-6">
                        <h3>C3D</h3>
                        <br/>
                        <CodeMirror
                            value={estado.c3d}
                            height="500px"
                            theme={xcodeDark}
                            extensions={[StreamLanguage.define(go)]}
                            onChange={(value) => {
                                setEstado({ ...estado, c3d: value});
                            }}
                        />
                        <br/>
                    </div>
                </div>
        </div>
    )
}
