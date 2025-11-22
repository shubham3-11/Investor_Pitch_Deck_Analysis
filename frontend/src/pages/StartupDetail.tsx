import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { api } from '../api';
import type { Startup } from '../api';

export default function StartupDetail() {
    const { id } = useParams<{ id: string }>();
    const [startup, setStartup] = useState<Startup | null>(null);
    const [file, setFile] = useState<File | null>(null);
    const [uploading, setUploading] = useState(false);

    useEffect(() => {
        if (id) loadStartup(id);
    }, [id]);

    const loadStartup = async (startupId: string) => {
        const data = await api.getStartup(startupId);
        setStartup(data);
    };

    const handleUpload = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!file || !startup) return;
        setUploading(true);
        try {
            await api.uploadDeck(startup.id, file);
            alert("Deck uploaded! Analysis will start in the background.");
            loadStartup(startup.id.toString());
            setFile(null);
        } catch (err) {
            console.error(err);
            alert("Upload failed");
        } finally {
            setUploading(false);
        }
    };

    if (!startup) return <div>Loading...</div>;

    return (
        <div className="container">
            <Link to="/" className="back-link">← Back to Startups</Link>
            <h1>{startup.name}</h1>
            <p>{startup.description}</p>
            {startup.website && <p><a href={startup.website} target="_blank" rel="noreferrer">{startup.website}</a></p>}

            <div className="card">
                <h2>Upload Pitch Deck</h2>
                <form onSubmit={handleUpload}>
                    <input
                        type="file"
                        accept="application/pdf"
                        onChange={e => setFile(e.target.files ? e.target.files[0] : null)}
                        required
                    />
                    <button type="submit" disabled={uploading}>
                        {uploading ? "Uploading..." : "Upload PDF"}
                    </button>
                </form>
            </div>

            <h2>Decks</h2>
            <table className="table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Uploaded At</th>
                        <th>Status</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    {startup.decks?.map(d => (
                        <tr key={d.id}>
                            <td>{d.id}</td>
                            <td>{new Date(d.created_at).toLocaleString()}</td>
                            <td>{d.processed ? "Processed" : "Processing..."}</td>
                            <td>
                                <Link to={`/decks/${d.id}`}>View Analysis</Link>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}
