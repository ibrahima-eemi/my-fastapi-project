import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Home from './components/Home';
import CreateMember from './components/CreateMember';
import CreateEvent from './components/CreateEvent';
import './App.css';

function App() {
  return (
    <Router>
      <div>
        <header>
          <h1>Sports Association Management</h1>
        </header>
        <Switch>
          <Route path="/" exact component={Home} />
          <Route path="/create-member" component={CreateMember} />
          <Route path="/create-event" component={CreateEvent} />
        </Switch>
      </div>
    </Router>
  );
}

export default App;
