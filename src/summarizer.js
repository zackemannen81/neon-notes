// src/summarizer.js

export function summarizeNote(content) {
    if (content.trim() === '') {
        return { tldr: 'Nothing to summarize.', highlights: [] };
    }

    // Mock summarization logic
    const tldr = `TL;DR: This is a mock summary of your note.`;
    const highlights = [
        'Key point one.',
        'Key point two.',
        'Key point three.'
    ];

    return { tldr, highlights };
}
