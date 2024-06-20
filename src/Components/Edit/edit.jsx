/* eslint-disable react/prop-types */
// import { useNavigate } from "react-router"


const Edit = ({ isEditing, handleEdit, handleSave }) => {
  // const navigate = useNavigate()

  // const editTodo = () => {
  //   fetch(`http://127.0.0.1:8000/api/${id}`, {
  //     method: "PUT",
  //     body: JSON.stringify({
  //       id: id
  //     })
  //   }).then(response => response.json())
  //   .then(data => {
  //     console.log(data)
  //     navigate("/")
  //   })
  // }

  let styles = {
    backgroundColor: "cadetblue",
    color: "white",
    marginLeft: "10px"
  }

  return (
    <>      
      <button style={styles} onClick={isEditing ? handleSave : handleEdit} >{isEditing? "Save" : "Edit"}</button>
    </>
  )
}

export default Edit