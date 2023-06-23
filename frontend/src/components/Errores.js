
export function Errores(props) {
    return(
        <div className="container">
            <div>
                <h1 className="titulo">Tabla de Errores</h1>
                <br/>
            </div>
            <div>
                <table className="table table-striped table-hover table-dark">
                    <thead style={{ textAlign: 'center' }}>
                        <tr className="table-success">
                            <th scope="col">No.</th>
                            <th scope="col">Tipo</th>
                            <th scope="col">Descripción</th>
                            <th scope="col">Línea</th>
                            <th scope="col">Columna</th>
                        </tr>
                    </thead>
                    <tbody style={{ textAlign: 'center' }} className="table-group-divider">
                        { props.rep.map(
                            element => 
                            <tr key={element.numero}>
                                <td>{element.numero}</td>
                                <td>{element.tipo}</td>
                                <td>{element.desc}</td>
                                <td>{element.fila}</td>
                                <td>{element.colum}</td>
                            </tr>
                        )}
                        
                    </tbody>
                </table>
            </div>
        </div>
    )
}
