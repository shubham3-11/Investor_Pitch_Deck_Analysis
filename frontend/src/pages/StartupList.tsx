import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../api';
import type { Startup } from '../api';

export default function StartupList() {
    const [startups, setStartups] = useState<Startup[]>([]);
    const [newStartup, setNewStartup] = useState({ name: '', website: '', description: '' });

    useEffect(() => {
        loadStartups();
    }, []);

    const loadStartups = async () => {
        const data = await api.getStartups();
        setStartups(data);
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!newStartup.name) return;
        await api.createStartup(newStartup);
        setNewStartup({ name: '', website: '', description: '' });
        loadStartups();
    };

    return (
        <div className="container">
            <h1>Startups</h1>

            <div className="card">
                <h2>Add New Startup</h2>
                <form onSubmit={handleSubmit} className="form-inline">
                    <input
                        placeholder="Name"
                        value={newStartup.name}
                        onChange={e => setNewStartup({ ...newStartup, name: e.target.value })}
                        required
                    />
                    <input
                        placeholder="Website"
                        value={newStartup.website}
                        onChange={e => setNewStartup({ ...newStartup, website: e.target.value })}
                    />
                    <input
                        placeholder="Description"
                        value={newStartup.description}
                        onChange={e => setNewStartup({ ...newStartup, description: e.target.value })}
                    />
                    <button type="submit">Add</button>
                </form>
            </div>

            <table className="table">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Website</th>
                        <th>Decks</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    {startups.map(s => (
                        <tr key={s.id}>
                            <td>{s.name}</td>
                            <td>{s.website && <a href={s.website} target="_blank" rel="noreferrer">{s.website}</a>}</td>
                            <td>{s.number_of_decks}</td>
                            <td><Link to={`/startups/${s.id}`}>View</Link></td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}
