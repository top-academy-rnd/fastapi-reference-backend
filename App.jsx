import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import heroImg from './assets/hero.png'
import './App.css'

function RegistrationForm() {
  const [formData, setFormData] = useState({ login: '', password: '' });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  // Replace this with your actual backend function
  const sendDataToBackend = async (userData) => {
    const userDataJson = JSON.stringify(userData);
    // '{"login": "asdfa", "password": "12345"}'
    console.log('Sending data to backend:', userData);
    await fetch('http://127.0.0.1:8000/users', { 
      method: 'POST', 
      body: userDataJson,
      headers: {"Content-Type": "application/json"}
    });
    // POST /users HTTP/1.1
    // Content-Type: application/json
    // 
    // {"login": "asdfa", "password": "12345"}
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    sendDataToBackend(formData);
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>Login:</label>
        <input name="login" value={formData.login} onChange={handleInputChange} required />
      </div>
      <div>
        <label>Password:</label>
        <input type="password" name="password" value={formData.userData} onChange={handleInputChange} required />
      </div>
      <button type="submit">Register</button>
    </form>
  );
}


function LoginForm() {
  const [formData, setFormData] = useState({ login: '', password: '' });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const sendDataToBackend = async (userData) => {
    const userDataJson = JSON.stringify(userData);
    // '{"login": "asdfa", "password": "12345"}'
    console.log('Sending data to backend:', userData);
    result = await fetch('http://127.0.0.1:8000/session', { 
      method: 'POST', 
      body: userDataJson,
      headers: {"Content-Type": "application/json"}
    });
    // Как выглядит запрос:
    //
    // POST /session HTTP/1.1
    // Content-Type: application/json
    // 
    // {"login": "asdfa", "password": "12345"}

    session_data = await result.json();
    session_secret = session_data["secret"];

    localStorage.setItem('current_session', session_data);  // {secret: "asfhrthgew4re", user_id: 6}
  
    //  Пример запроса в рамках текущей сессии входа в аккаунт

    current_session_data = localStorage.getItem('current_session');

    url = "http://127.0.0.1:8000/users/" + current_session_data["user_id"] + "/cart/items"
    await fetch(
      url,
      {
        body: '{"product_id": 5}',
        header: {"Session-Secret": current_session_data["secret"]},
      }
    )
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    sendDataToBackend(formData);
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>Login:</label>
        <input name="login" value={formData.login} onChange={handleInputChange} required />
      </div>
      <div>
        <label>Password:</label>
        <input type="password" name="password" value={formData.userData} onChange={handleInputChange} required />
      </div>
      <button type="submit">Register</button>
    </form>
  );
}


function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <h2>Регистрация</h2>
      <RegistrationForm />
    </>
  )
}

export default App
