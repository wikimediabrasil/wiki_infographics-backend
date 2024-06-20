/* eslint-disable react/prop-types */
import { useNavigate } from "react-router"


const Delete = ({ id }) => {
  const navigate = useNavigate()

  const deleteTodo = () => {
    fetch(`http://127.0.0.1:8000/api/${id}`, {
      method: "DELETE",
      body: JSON.stringify({
        id: id
      })
    }).then(response => response.json())
    .then(data => {
      console.log(data)
      navigate("/")
    })
  }

  let styles = { backgroundColor: "red",
    color: "white"
  }

  return (
    <>      
      <button style={styles} onClick={deleteTodo}>Delete</button>
    </>
  )
}

export default Delete