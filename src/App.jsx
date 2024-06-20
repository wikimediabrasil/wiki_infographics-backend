import {
  BrowserRouter as Router,
  Routes,
  Route,
  // Link
} from "react-router-dom"
import TodoPage from './Pages/TodoPage'
import Show from "./Pages/Show"
import './App.css'


const App = () => {

  return (
    <Router>
      <Routes>
        <Route path="/:id" element={<Show/>} /> 
        <Route path="/" element={<TodoPage/>} /> 
      </Routes>
    </Router> 
  )
}

export default App
