import React, { useState } from 'react';
import axios from 'axios';
import './Form.css';

const CreateEvent = () => {
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    category: '',
    level: '',
    age_group: '',
    is_paid: false,
    fee: 0
  });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post('http://127.0.0.1:8000/events/', formData);
      alert('Event created successfully!');
    } catch (error) {
      console.error('Error creating event:', error);
      alert('Failed to create event');
    }
  };

  return (
    <div className="form-container">
      <h2>Create Event</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Name:</label>
          <input type="text" name="name" value={formData.name} onChange={handleChange} required />
        </div>
        <div className="form-group">
          <label>Description:</label>
          <input type="text" name="description" value={formData.description} onChange={handleChange} required />
        </div>
        <div className="form-group">
          <label>Category:</label>
          <input type="text" name="category" value={formData.category} onChange={handleChange} required />
        </div>
        <div className="form-group">
          <label>Level:</label>
          <input type="text" name="level" value={formData.level} onChange={handleChange} required />
        </div>
        <div className="form-group">
          <label>Age Group:</label>
          <input type="text" name="age_group" value={formData.age_group} onChange={handleChange} required />
        </div>
        <div className="form-group">
          <label>Is Paid:</label>
          <input type="checkbox" name="is_paid" checked={formData.is_paid} onChange={handleChange} />
        </div>
        <div className="form-group">
          <label>Fee:</label>
          <input type="number" name="fee" value={formData.fee} onChange={handleChange} required />
        </div>
        <button type="submit">Create Event</button>
      </form>
    </div>
  );
};

export default CreateEvent;
