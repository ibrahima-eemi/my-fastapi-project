import React, { useState } from 'react';
import axios from 'axios';
import './Form.css';

const CreateMember = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [category, setCategory] = useState('');
  const [level, setLevel] = useState('');
  const [ageGroup, setAgeGroup] = useState('');
  const [isActive, setIsActive] = useState(true);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://127.0.0.1:8000/members/', {
        name,
        email,
        category,
        level,
        age_group: ageGroup,
        is_active: isActive
      });
      console.log('Response:', response); // Use the response variable here
      alert('Member created successfully');
    } catch (error) {
      console.error('Failed to create member', error);
      alert('Failed to create member');
    }
  };

  return (
    <div className="form-container">
      <h2>Create Member</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Name:</label>
          <input type="text" value={name} onChange={(e) => setName(e.target.value)} required />
        </div>
        <div className="form-group">
          <label>Email:</label>
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        </div>
        <div className="form-group">
          <label>Category:</label>
          <input type="text" value={category} onChange={(e) => setCategory(e.target.value)} required />
        </div>
        <div className="form-group">
          <label>Level:</label>
          <input type="text" value={level} onChange={(e) => setLevel(e.target.value)} required />
        </div>
        <div className="form-group">
          <label>Age Group:</label>
          <input type="text" value={ageGroup} onChange={(e) => setAgeGroup(e.target.value)} required />
        </div>
        <div className="form-group">
          <label>Is Active:</label>
          <input type="checkbox" checked={isActive} onChange={(e) => setIsActive(e.target.checked)} />
        </div>
        <button type="submit">Create Member</button>
      </form>
    </div>
  );
};

export default CreateMember;
