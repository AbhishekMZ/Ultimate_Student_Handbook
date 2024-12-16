document.addEventListener('DOMContentLoaded', () => {
    // Tab Navigation
    const tabs = document.querySelectorAll('.nav-links a');
    const sections = document.querySelectorAll('.content-section');

    tabs.forEach(tab => {
        tab.addEventListener('click', (e) => {
            e.preventDefault();
            // Remove active class from all tabs and sections
            tabs.forEach(t => t.classList.remove('active'));
            sections.forEach(s => s.classList.remove('active'));
            
            // Add active class to clicked tab
            tab.classList.add('active');
            
            // Show corresponding section
            const sectionId = tab.id.replace('-tab', '-section');
            document.getElementById(sectionId).classList.add('active');
        });
    });

    // Notes Functionality
    const notesContainer = document.getElementById('notes-container');
    const addNoteBtn = document.getElementById('add-note-btn');
    const addNoteModal = document.getElementById('add-note-modal');
    const addNoteForm = document.getElementById('add-note-form');

    // Load Notes
    const loadNotes = async () => {
        try {
            const response = await fetch('/api/notes');
            const data = await response.json();
            if (data.success) {
                notesContainer.innerHTML = data.notes.map(note => `
                    <div class="note-card">
                        <h3>${note.title}</h3>
                        <p>${note.content}</p>
                        <div class="note-footer">
                            <span class="date">${new Date(note.created_at).toLocaleDateString()}</span>
                        </div>
                    </div>
                `).join('');
            }
        } catch (error) {
            console.error('Error loading notes:', error);
        }
    };

    // Add Note
    addNoteBtn.addEventListener('click', () => {
        addNoteModal.style.display = 'flex';
    });

    addNoteForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(addNoteForm);
        try {
            const response = await fetch('/api/notes', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    title: formData.get('title'),
                    content: formData.get('content')
                })
            });
            const data = await response.json();
            if (data.success) {
                addNoteModal.style.display = 'none';
                addNoteForm.reset();
                loadNotes();
            }
        } catch (error) {
            console.error('Error adding note:', error);
        }
    });

    // Tasks Functionality
    const tasksContainer = document.getElementById('tasks-container');
    const addTaskBtn = document.getElementById('add-task-btn');
    const addTaskModal = document.getElementById('add-task-modal');
    const addTaskForm = document.getElementById('add-task-form');

    // Load Tasks
    const loadTasks = async () => {
        try {
            const response = await fetch('/api/tasks');
            const data = await response.json();
            if (data.success) {
                tasksContainer.innerHTML = data.tasks.map(task => `
                    <div class="task-card ${task.status}">
                        <div class="task-header">
                            <h3>${task.title}</h3>
                            <span class="due-date">Due: ${new Date(task.due_date).toLocaleDateString()}</span>
                        </div>
                        <p>${task.description}</p>
                        <div class="task-footer">
                            <span class="status">${task.status}</span>
                        </div>
                    </div>
                `).join('');
            }
        } catch (error) {
            console.error('Error loading tasks:', error);
        }
    };

    // Add Task
    addTaskBtn.addEventListener('click', () => {
        addTaskModal.style.display = 'flex';
    });

    addTaskForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(addTaskForm);
        try {
            const response = await fetch('/api/tasks', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    title: formData.get('title'),
                    description: formData.get('description'),
                    due_date: formData.get('due_date')
                })
            });
            const data = await response.json();
            if (data.success) {
                addTaskModal.style.display = 'none';
                addTaskForm.reset();
                loadTasks();
            }
        } catch (error) {
            console.error('Error adding task:', error);
        }
    });

    // Modal Close Buttons
    document.querySelectorAll('.cancel-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.modal').forEach(modal => {
                modal.style.display = 'none';
            });
        });
    });

    // Initial Load
    loadNotes();
    loadTasks();
});
