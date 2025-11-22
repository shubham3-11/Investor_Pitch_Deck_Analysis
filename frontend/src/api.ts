const API_BASE = "http://localhost:8000/api";

export interface Startup {
    id: number;
    name: string;
    website?: string;
    description?: string;
    created_at: string;
    number_of_decks?: number;
    latest_deck_id?: number;
    decks?: Deck[];
}

export interface Deck {
    id: number;
    startup_id: number;
    created_at: string;
    processed: boolean;
    summary?: any;
    claims?: Claim[];
    questions?: Question[];
}

export interface Claim {
    id: number;
    text: string;
    category: string;
    plausibility_score: number;
    notes: string;
}

export interface Question {
    id: number;
    text: string;
    category: string;
}

export const api = {
    getStartups: async (): Promise<Startup[]> => {
        const res = await fetch(`${API_BASE}/startups`);
        return res.json();
    },

    getStartup: async (id: string): Promise<Startup> => {
        const res = await fetch(`${API_BASE}/startups/${id}`);
        return res.json();
    },

    createStartup: async (data: { name: string; website?: string; description?: string }) => {
        const res = await fetch(`${API_BASE}/startups`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });
        return res.json();
    },

    uploadDeck: async (startupId: number, file: File) => {
        const formData = new FormData();
        formData.append("startup_id", startupId.toString());
        formData.append("file", file);

        const res = await fetch(`${API_BASE}/decks`, {
            method: "POST",
            body: formData,
        });
        return res.json();
    },

    getDeck: async (id: string): Promise<Deck> => {
        const res = await fetch(`${API_BASE}/decks/${id}`);
        return res.json();
    }
};
