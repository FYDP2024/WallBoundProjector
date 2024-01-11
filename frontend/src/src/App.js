import logo from './logo.svg';
import './App.css';
import Canvas from './components/Canvas';
import Sidebar from './components/Sidebar';

function App() {
  return (
    <div className="App">
      <Sidebar />
      <div className='workspace'>
        <Canvas />
      </div>
      
    </div>
  );
}

export default App;
