import { useState, useEffect } from "react"
import { useParams, useNavigate } from "react-router"
import { Link } from "react-router-dom"

import Delete from "../Components/Delete/delete"
import Edit from "../Components/Edit/edit"


const Show = () => {
  const navigate = useNavigate()
  const {id} = useParams()
  const [todo, setTodo] = useState([])
  const [updateTodo, setUpdtaeTodo] = useState("")
  const [isEditing, setIsEditing] = useState(false)
  
  
  
  useEffect(() => {
    fetch(`http://127.0.0.1:8000/api/${id}`).then(response => response.json())
    .then(data => {
      setTodo(data)})
  },[id])

  const handleChange = (event) => {
    setUpdtaeTodo(event.target.value)
    // console.log(updateTodo)
  }

  const handleUpdateSubmit = () => {
    // console.log({updateTodo, })
    fetch(`http://127.0.0.1:8000/api/${id}`, {
      method: "PUT",
      body: JSON.stringify({
        content: updateTodo
      }),
      headers: {
        "Cotent-Type": "application/json; charset=UTF-8"
      }
    })
    .then(response => response.json())
    .then(message => {
      console.log(message)
      setUpdtaeTodo("")
      navigate("/")
    })
  }

  const handleSave = (event) => {
    event.preventDefault()
    handleUpdateSubmit()
  }

  const handleEdit = () => {
    setIsEditing(true)
    todo.map(data => (setUpdtaeTodo(data.content))) 
  }

  return (
    <div>
      {isEditing && <input type="text" value={updateTodo} onChange={handleChange}/>}
      {todo.length > 0 && todo.map(data => 
        (<div key={data.id}>{data.content}</div>)
      )}
      {!isEditing && <Delete id={id}/>}
      <Edit isEditing={isEditing} handleEdit={handleEdit} handleSave={handleSave}id={id}/>
      <hr />
      <Link to="/">Back to todos</Link>
    </div>
  )
}

export default Show