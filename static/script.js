document.addEventListener('DOMContentLoaded', loadTodos);
document.getElementById('todoForm').addEventListener('submit', addTodo);

async function loadTodos() {
    const response = await fetch('/todos');
    const todos = await response.json();
    const list = document.getElementById('todoList');
    list.innerHTML = '';
    
    todos.forEach(todo => {
        const li = document.createElement('li');
        li.innerHTML = `
            <input type="checkbox" ${todo.completed ? 'checked' : ''}>
            <span class="${todo.completed ? 'completed' : ''}">${todo.task}</span>
            <button class="deleteBtn">🗑️</button>
        `;
        li.querySelector('input').addEventListener('change', () => toggleTodo(todo.id));
        li.querySelector('.deleteBtn').addEventListener('click', () => deleteTodo(todo.id));
        list.appendChild(li);
    });
}

async function addTodo(e) {
    e.preventDefault();
    const taskInput = document.getElementById('taskInput');
    await fetch('/add', {
        method: 'POST',
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: `task=${encodeURIComponent(taskInput.value)}`
    });
    taskInput.value = '';
    loadTodos();
}

async function deleteTodo(id) {
    await fetch('/delete', {
        method: 'POST',
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: `id=${id}`
    });
    loadTodos();
}

async function toggleTodo(id) {
    await fetch('/toggle', {
        method: 'POST',
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: `id=${id}`
    });
    loadTodos();
}