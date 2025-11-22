import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { api } from '../api';
import type { Deck } from '../api';

export default function DeckAnalysis() {
    const { deckId } = useParams<{ deckId: string }>();
    const [deck, setDeck] = useState<Deck | null>(null);

    useEffect(() => {
        if (deckId) {
            loadDeck(deckId);
            // Poll every 10 seconds if not processed
            const interval = setInterval(() => {
                loadDeck(deckId);
            }, 10000);
            return () => clearInterval(interval);
        }
    }, [deckId]);

    const loadDeck = async (id: string) => {
        const data = await api.getDeck(id);
        setDeck(data);
    };

    if (!deck) return <div>Loading...</div>;

    if (!deck.processed) {
        return (
            <div className="container">
                <Link to={`/startups/${deck.startup_id}`} className="back-link">← Back to Startup</Link>
                <h1>Deck Analysis #{deck.id}</h1>
                <div className="card">
                    <p>Analysis in progress. This page will auto-refresh.</p>
                </div>
            </div>
        );
    }

    const { summary, claims, questions } = deck;

    return (
        <div className="container">
            <Link to={`/startups/${deck.startup_id}`} className="back-link">← Back to Startup</Link>
            <h1>Deck Analysis #{deck.id}</h1>

            <div className="section">
                <h2>Summary</h2>
                <div className="grid">
                    {Object.entries(summary || {}).map(([key, value]) => (
                        <div key={key} className="card">
                            <h3>{key.charAt(0).toUpperCase() + key.slice(1)}</h3>
                            <p>{String(value)}</p>
                        </div>
                    ))}
                </div>
            </div>

            <div className="section">
                <h2>Claims Assessment</h2>
                <table className="table">
                    <thead>
                        <tr>
                            <th>Category</th>
                            <th>Claim</th>
                            <th>Score</th>
                            <th>Notes</th>
                        </tr>
                    </thead>
                    <tbody>
                        {claims?.map(c => (
                            <tr key={c.id}>
                                <td><span className="badge">{c.category}</span></td>
                                <td>{c.text}</td>
                                <td>
                                    <div className="score-bar">
                                        <div
                                            className="score-fill"
                                            style={{
                                                width: `${(c.plausibility_score || 0) * 100}%`,
                                                backgroundColor: (c.plausibility_score || 0) > 0.7 ? '#4caf50' : (c.plausibility_score || 0) > 0.4 ? '#ff9800' : '#f44336'
                                            }}
                                        ></div>
                                        <span>{((c.plausibility_score || 0) * 10).toFixed(1)}/10</span>
                                    </div>
                                </td>
                                <td>{c.notes}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            <div className="section">
                <h2>Follow-up Questions</h2>
                <ul className="list">
                    {questions?.map(q => (
                        <li key={q.id} className="list-item">
                            <strong>[{q.category}]</strong> {q.text}
                        </li>
                    ))}
                </ul>
            </div>
        </div>
    );
}
