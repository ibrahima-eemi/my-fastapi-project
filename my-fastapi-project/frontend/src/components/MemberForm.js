import React, { useState } from 'react';
import axios from 'axios';
import './Form.css';

const MemberForm = () => {
    const [member, setMember] = useState({
        name: '',
        email: '',
        category: '',
        level: '',
        age_group: '',
    });

    const handleChange = (e) => {
        setMember({
            ...member,
            [e.target.name]: e.target.value,
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://localhost:8000/members/', member);
            console.log(response.data);
            alert('Member created successfully!');
        } catch (error) {
            console.error(error);
            alert('Error creating member.');
        }
    };

    return (
        <form className="form-container" onSubmit={handleSubmit}>
            <h2>Register Member</h2>
            <label>Name</label>
            <input type="text" name="name" value={member.name} onChange={handleChange} required />
            
            <label>Email</label>
            <input type="email" name="email" value={member.email} onChange={handleChange} required />
            
            <label>Category</label>
            <select name="category" value={member.category} onChange={handleChange} required>
                <option value="">Select Category</option>
                <option value="classique">Classique</option>
                <option value="modern jazz">Modern Jazz</option>
                <option value="contemporain">Contemporain</option>
                <option value="hip-hop">Hip-Hop</option>
            </select>
            
            <label>Level</label>
            <select name="level" value={member.level} onChange={handleChange} required>
                <option value="">Select Level</option>
                <option value="éveil/initiation">Éveil/Initiation</option>
                <option value="débutant">Débutant</option>
                <option value="intermédiaire">Intermédiaire</option>
                <option value="confirmé">Confirmé</option>
                <option value="avancé">Avancé</option>
            </select>
            
            <label>Age Group</label>
            <select name="age_group" value={member.age_group} onChange={handleChange} required>
                <option value="">Select Age Group</option>
                <option value="enfant">Enfant</option>
                <option value="adolescent">Adolescent</option>
                <option value="jeune adulte">Jeune Adulte</option>
                <option value="adulte">Adulte</option>
            </select>
            
            <button type="submit">Submit</button>
        </form>
    );
};

export default MemberForm;
