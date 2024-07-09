import React from 'react';
import { Link } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPlus } from '@fortawesome/free-solid-svg-icons';
import './Home.css';

const Home = () => {
  return (
    <div className="container">
      <h2>Welcome to the Sports Association Management</h2>
      <div className="links">
        <Link to="/create-member">
          <FontAwesomeIcon icon={faPlus} /> Create Member
        </Link>
        <Link to="/create-event">
          <FontAwesomeIcon icon={faPlus} /> Create Event
        </Link>
      </div>
    </div>
  );
};

export default Home;
