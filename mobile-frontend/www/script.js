document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('todoForm');
    form.addEventListener('submit', addTodo);
    loadTodos();
});

// async function loadTodos() {
//     try {
//         const response = await fetch('/todos');
//         const todos = await response.json();
//         const list = document.getElementById('todoList');
//         list.innerHTML = '';

//         todos.forEach(todo => {
//             const li = document.createElement('li');
//             li.innerHTML = `
//                 <input type="checkbox" ${todo.completed ? 'checked' : ''}>
//                 <span class="${todo.completed ? 'completed' : ''}">${todo.task}</span>
//                 <button class="deleteBtn">Delete</button>
//             `;

//             li.querySelector('input').addEventListener('change', () => toggleTodo(todo.id));
//             li.querySelector('.deleteBtn').addEventListener('click', () => deleteTodo(todo.id));
//             list.appendChild(li);
//         });
//     } catch (error) {
//         console.error('Failed to load todos:', error);
//     }
// }
const BASE_URL = 'http://192.168.101.31:8000';

async function loadTodos() {
    try {
        const response = await fetch(`${BASE_URL}/todos`);
        const todos = await response.json();
        const list = document.getElementById('todoList');
        list.innerHTML = '';

        todos.forEach(todo => {
            const li = document.createElement('li');
            li.innerHTML = `
                <input type="checkbox" ${todo.completed ? 'checked' : ''}>
                <span class="${todo.completed ? 'completed' : ''}">${todo.task}</span>
                <button class="deleteBtn">Delete</button>
            `;

            li.querySelector('input').addEventListener('change', () => toggleTodo(todo.id));
            li.querySelector('.deleteBtn').addEventListener('click', () => deleteTodo(todo.id));
            list.appendChild(li);
        });
    } catch (error) {
        console.error('Failed to load todos:', error);
    }
}

async function addTodo(e) {
    e.preventDefault();
    const taskInput = document.getElementById('taskInput');
    if (!taskInput.value.trim()) return;

    try {
        await fetch(`${BASE_URL}/add`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: `task=${encodeURIComponent(taskInput.value)}`
        });
        taskInput.value = '';
        loadTodos();
    } catch (error) {
        console.error('Failed to add todo:', error);
    }
}

async function deleteTodo(id) {
    try {
        await fetch(`${BASE_URL}/delete`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: `id=${id}`
        });
        loadTodos();
    } catch (error) {
        console.error('Failed to delete todo:', error);
    }
}

async function toggleTodo(id) {
    try {
        await fetch(`${BASE_URL}/toggle`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: `id=${id}`
        });
        loadTodos();
    } catch (error) {
        console.error('Failed to toggle todo:', error);
    }
}

