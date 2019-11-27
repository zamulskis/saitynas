import React from 'react';
// import logo from './logo.svg';
import './App.css';
import { Button, Form } from 'react-bootstrap';
import { BrowserRouter as Router, Route, Link } from "react-router-dom";


function App() {
    return (
    <Router>
      <div>
        <ul>
          <li>
            <Link to="/">Home</Link>
          </li>
          <li>
            <Link to="/about">About</Link>
          </li>
          <li>
            <Link to="/topics">Topics</Link>
          </li>
        </ul>

        <hr />

        {/* <Route exact path="/" />
        <Route path="/about"  /> */}
        <Route path="/topics" component={Register} />
      </div>
    </Router>
  );
}
function Register() {
  return (
    <Form>
      <Form.Group controlId="formBasicEmail">
        <Form.Label>Email address</Form.Label>
        <Form.Control type="email" placeholder="Enter email" />
        <Form.Text className="text-muted">
          We'll never share your email with anyone else.
    </Form.Text>
      </Form.Group>

      <Form.Group controlId="formBasicPassword">
        <Form.Label>Password</Form.Label>
        <Form.Control type="password" placeholder="Password" />
      </Form.Group>
      <Form.Group controlId="formBasicCheckbox">
        <Form.Check type="checkbox" label="Check me out" />
      </Form.Group>
      <Button variant="primary" type="submit">
        Submit
  </Button>
    </Form>
  );
}

export default App;
