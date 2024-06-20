import { useState, useEffect } from 'react'
import Card from '../Components/Card/card'
import Form from '../Components/Form/form'

const TodoPage = () => {

  const [todo, setTodo] = useState([])
  const [addTodo, setAddTodo] = useState("")

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api").then(response => {
      if(response.ok){
        return response.json()
      }
    }).then(data => setTodo(data))
    .catch((err) => console.log(err))
  },[])

  const handleFormChange = (inputValue) => {
    setAddTodo(inputValue)
  }

  const handleFormSubmit = () => {
    fetch("http://127.0.0.1:8000/api/create", {
      method: "POST",
      body: JSON.stringify({
        content: addTodo
      }),
      headers: {
        "Cotent-Type": "application/json; charset=UTF-8"
      }
    })
    .then(response => response.json())
    .then(message => {
      console.log(message)
      setAddTodo("")
      getLastestTodos()
    })   
  }

  const getLastestTodos = () => {
    fetch("http://127.0.0.1:8000/api").then(response => {
      if(response.ok){
        return response.json()
      }
    }).then(data => setTodo(data))
  }
  
  return (
    <>
      <Form userInput={addTodo} onFormChange={handleFormChange} onFormSubmit={handleFormSubmit}/>
      <Card listOfTodos={todo}/>
    </>
  )
}

export default TodoPage