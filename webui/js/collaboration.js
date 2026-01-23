const socket = io();
const editor = document.getElementById('editor');
const statusDiv = document.getElementById('status');
const docId = 'default';

socket.on('connect', () => {
    statusDiv.textContent = 'Connected';
    console.log('Connected to server');
    socket.emit('join_document', { doc_id: docId });
});

socket.on('disconnect', () => {
    statusDiv.textContent = 'Disconnected';
    console.log('Disconnected from server');
});

socket.on('document_state', (data) => {
    console.log('Received document state');
    editor.value = data.content;
});

socket.on('document_updated', (data) => {
    console.log('Received document update');
    // Save cursor position
    const start = editor.selectionStart;
    const end = editor.selectionEnd;
    
    editor.value = data.content;
    
    // Restore cursor
    // This is naive and will be incorrect if text was inserted before cursor
    // But sufficient for a prototype
    editor.setSelectionRange(start, end);
});

editor.addEventListener('input', () => {
    const content = editor.value;
    socket.emit('update_document', { doc_id: docId, content: content });
});
