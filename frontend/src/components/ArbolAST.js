
export function ArbolAST(props) {

    return(
        <div className="container">
            <div>
                <h1 className="titulo">Árbol de Análisis Sintáctico</h1>
                <br/>
            </div>
            <div>
                <img src={`data:image/svg+xml;base64,${props.rep}`} alt='CST' />
            </div>
        </div>
    )
}

