import React, { useState } from 'react';
import axios from 'axios';
import './Form.css';

const EventForm = () => {
    const [event, setEvent] = useState({
        name: '',
        description: '',
        category: '',
        level: '',
        age_group: '',
        is_paid: false,
        fee: 0,
    });

    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;
        setEvent({
            ...event,
            [name]: type === 'checkbox' ? checked : value,
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://localhost:8000/events/', event);
            console.log(response.data);
            alert('Event created successfully!');
        } catch (error) {
            console.error(error);
            alert('Error creating event.');
        }
    };

    return (
        <form className="form-container" onSubmit={handleSubmit}>
            <h2>Create Event</h2>
            <label>Name</label>
            <input type="text" name="name" value={event.name} onChange={handleChange} required />
            
            <label>Description</label>
            <input type="text" name="description" value={event.description} onChange={handleChange} required />
            
            <label>Category</label>
            <select name="category" value={event.category} onChange={handleChange} required>
                <option value="">Select Category</option>
                <option value="classique">Classique</option>
                <option value="modern jazz">Modern Jazz</option>
                <option value="contemporain">Contemporain</option>
                <option value="hip-hop">Hip-Hop</option>
            </select>
            
            <label>Level</label>
            <select name="level" value={event.level} onChange={handleChange} required>
                <option value="">Select Level</option>
                <option value="éveil/initiation">Éveil/Initiation</option>
                <option value="débutant">Débutant</option>
                <option value="intermédiaire">Intermédiaire</option>
                <option value="confirmé">Confirmé</option>
                <option value="avancé">Avancé</option>
            </select>
            
            <label>Age Group</label>
            <select name="age_group" value={event.age_group} onChange={handleChange} required>
                <option value="">Select Age Group</option>
                <option value="enfant">Enfant</option>
                <option value="adolescent">Adolescent</option>
                <option value="jeune adulte">Jeune Adulte</option>
                <option value="adulte">Adulte</option>
            </select>
            
            <label>
                <input type="checkbox" name="is_paid" checked={event.is_paid} onChange={handleChange} />
                Paid Event
            </label>
            
            {event.is_paid && (
                <>
                    <label>Fee</label>
                    <input type="number" name="fee" value={event.fee} onChange={handleChange} required />
                </>
            )}
            
            <button type="submit">Submit</button>
        </form>
    );
};

export default EventForm;
