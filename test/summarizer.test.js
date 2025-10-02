// test/summarizer.test.js

import { summarizeNote } from '../src/summarizer.js';

function assert(condition, message) {
    if (!condition) {
        console.error('Assertion Failed:', message);
        throw new Error(message);
    }
    console.log('Assertion Passed:', message);
}

function runSummarizerTests() {
    console.log('--- Running Tests for Summarizer Mock ---');

    // Test 1: Empty content
    try {
        const result = summarizeNote('');
        assert(result.tldr === 'Nothing to summarize.', 'Test 1 Failed: Empty content should return specific TL;DR');
        assert(result.highlights.length === 0, 'Test 1 Failed: Empty content should return no highlights');
    } catch (e) {
        console.error('Test 1 Error:', e.message);
    }

    // Test 2: Non-empty content
    try {
        const content = 'This is a test note with some content that should be summarized.';
        const result = summarizeNote(content);
        assert(result.tldr.includes('TL;DR: This is a mock summary of your note.'), 'Test 2 Failed: Non-empty content should return mock TL;DR');
        assert(result.highlights.length === 3, 'Test 2 Failed: Non-empty content should return 3 highlights');
        assert(result.highlights[0] === 'Key point one.', 'Test 2 Failed: First highlight incorrect');
        assert(result.highlights[1] === 'Key point two.', 'Test 2 Failed: Second highlight incorrect');
        assert(result.highlights[2] === 'Key point three.', 'Test 2 Failed: Third highlight incorrect');
    } catch (e) {
        console.error('Test 2 Error:', e.message);
    }

    console.log('--- Summarizer Tests Finished ---');
}

runSummarizerTests();
