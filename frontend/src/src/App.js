import logo from './logo.svg';
import './App.css';
import Canvas from './components/Canvas';
import Sidebar from './components/Sidebar';

function App() {


  const images = [
    {
        url: "imgs/sample_img.png",
        width: 100,
        height: 100,
        x_pos: 300,
        y_pos: 300
    },
    {
        url: "imgs/terraria.png",
        width: 160,
        height: 200,
        x_pos: 200,
        y_pos: 80
    },
    {
      url: "imgs/poster.png",
      width: 140,
      height: 200,
      x_pos: 100,
      y_pos: 300
  },
]

  return (
    <div className="App">
      <Sidebar images={images}/>
      <div className='workspace'>
        <h1>Canvas</h1>
        <Canvas images={images}/>
      </div>
      
    </div>
  );
}

export default App;
