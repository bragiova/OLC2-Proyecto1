import React from 'react';
import { NavLink, Link } from 'react-router-dom';

export function Navbar(){
    return (
        <div>
            <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
                <div className='container-fluid'>
                    <Link className="navbar-brand" to='/'>PyTypeCraft</Link>
                    <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                        <span className="navbar-toggler-icon"></span>
                    </button>
                    <div className="collapse navbar-collapse" id="navbarSupportedContent">
                        <ul className="navbar-nav mr-auto">
                            <li className="nav-item">
                                <NavLink to='/' className={({isActive}) => (isActive) ? "nav-link active" : "nav-link"}>Home</NavLink>
                            </li>
                            <li className="nav-item">
                                <NavLink to='/editor' className={({isActive}) => (isActive) ? "nav-link active" : "nav-link"}>Editor</NavLink>
                            </li>
                            <li className="nav-item">
                                <NavLink to='/reportes' className={({isActive}) => (isActive) ? "nav-link active" : "nav-link"}>Reportes</NavLink>
                            </li>
                        </ul>
                    </div>
                </div>
            </nav>
        </div>
    )
}