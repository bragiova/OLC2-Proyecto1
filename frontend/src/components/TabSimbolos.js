
export function TablaSimbolos(props) {
    return(
        <div className="container">
            <div>
                <h1 className="titulo">Tabla de Símbolos</h1>
                <br/>
            </div>
            <div>
                <table className="table table-striped table-hover table-dark">
                    <thead style={{ textAlign: 'center' }}>
                        <tr className="table-success">
                            <th scope="col">No.</th>
                            <th scope="col">Nombre</th>
                            <th scope="col">Tipo</th>
                            <th scope="col">Ámbito</th>
                            <th scope="col">Fila</th>
                            <th scope="col">Columna</th>
                        </tr>
                    </thead>
                    <tbody style={{ textAlign: 'center' }} className="table-group-divider">
                        { props.rep.map(
                            element => 
                            <tr key={element.numero}>
                                <td>{element.numero}</td>
                                <td>{element.id}</td>
                                <td>{element.tipo}</td>
                                <td>{'prueba'}</td>
                                <td>{element.linea}</td>
                                <td>{element.colum}</td>
                            </tr>
                        )}
                        
                    </tbody>
                </table>
            </div>
        </div>
    )
}
