import { useEffect } from 'react';
// import Card from '../Components/Card/card';
// import Form from '../Components/Form/form';
import { useNavigate } from 'react-router';
import api from '../api/axios';

const OauthCallback = () => {
  // const [todo, setTodo] = useState([]);
  // const [addTodo, setAddTodo] = useState("");
  // const [userName, setUserName] = useState("")
  const navigate = useNavigate();


  useEffect(() => {
    const oauthAuthenticate = async () => {
    try {
      const queryString = window.location.search.substring(1);
      // console.log(queryString)
      const response = await api.post('/oauth-callback', { queryString: queryString });
      console.log(response.data.msg);
      if(response.data.msg === "Athentiaction sucessfull")
      navigate("/todos")
    } catch (err) {
      navigate("/")
    }
  };
  oauthAuthenticate();
  }, []);


  return (
    <>
      <h4> Authenticating..... </h4>
    </>
  );
};

export default OauthCallback;