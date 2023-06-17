import './App.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { Home } from './components/Home';
import { Navbar } from './components/Navbar';
import { Editor } from './components/Editor';
import { Reportes } from './components/Reportes';

function App() {
  return (
    <div className='App'>
      <Router>
        <Navbar/>
        <Routes>
          <Route exact path = '/' element = { <Home/> }/>
          <Route exact path = '/editor' element = { <Editor/> }/>
          <Route exact path = '/reportes' element = { <Reportes/> }/>
        </Routes>
      </Router>
    </div>
  );
}

export default App;
