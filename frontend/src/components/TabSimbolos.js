
export function TablaSimbolos() {
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
                        <tr>
                            <td>prueba</td>
                            <td>prueba</td>
                            <td>prueba</td>
                            <td>prueba</td>
                            <td>prueba</td>
                            <td>prueba</td>
                        </tr>
                        <tr>
                            <td>prueba</td>
                            <td>prueba</td>
                            <td>prueba</td>
                            <td>prueba</td>
                            <td>prueba</td>
                            <td>prueba</td>
                        </tr>
                        <tr>
                            <td>prueba</td>
                            <td>prueba</td>
                            <td>prueba</td>
                            <td>prueba</td>
                            <td>prueba</td>
                            <td>prueba</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    )
}
