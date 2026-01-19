const taskInput = document.getElementById('taskInput');
const addTaskBtn = document.getElementById('addTask');
const taskList = document.getElementById('taskList');

// Cargar tareas guardadas
function loadTasks() {
  const tasks = JSON.parse(localStorage.getItem('tasks')) || [];
  tasks.forEach(task => addTaskToDOM(task.text, task.completed));
}

// Agregar tarea al DOM
function addTaskToDOM(text, completed = false) {
  const li = document.createElement('li');
  li.innerHTML = `
    <span class="${completed ? 'completed' : ''}">${text}</span>
    <button class="delete-btn">🗑️</button>
  `;
  li.querySelector('span').addEventListener('click', () => {
    li.querySelector('span').classList.toggle('completed');
    saveTasks();
  });
  li.querySelector('.delete-btn').addEventListener('click', () => {
    li.remove();
    saveTasks();
  });
  taskList.appendChild(li);
}

// Guardar en localStorage
function saveTasks() {
  const tasks = [];
  document.querySelectorAll('#taskList li').forEach(li => {
    tasks.push({
      text: li.querySelector('span').textContent,
      completed: li.querySelector('span').classList.contains('completed')
    });
  });
  localStorage.setItem('tasks', JSON.stringify(tasks));
}

// Agregar tarea nueva
addTaskBtn.addEventListener('click', () => {
  const text = taskInput.value.trim();
  if (text) {
    addTaskToDOM(text);
    taskInput.value = '';
    saveTasks();
  }
});

taskInput.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') addTaskBtn.click();
});

// Cargar al inicio
loadTasks();