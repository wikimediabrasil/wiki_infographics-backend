import { useEffect } from 'react';
import { useNavigate } from 'react-router';
import api from '../api/axios';

const OauthCallback = () => {
  const navigate = useNavigate();


  useEffect(() => {
    const oauthAuthenticate = async () => {
    try {
      const queryString = window.location.search.substring(1);
      const response = await api.post('/oauth-callback', { queryString: queryString });
      console.log(response.data.msg);
      if(response.data.msg === "Athentiaction sucessfull")
      navigate("/todos")
    } catch (err) {
      navigate("/")
    }
  };
  oauthAuthenticate();
  }, [navigate]);


  return (
    <>
      <h4> Authenticating..... </h4>
    </>
  );
};

export default OauthCallback;