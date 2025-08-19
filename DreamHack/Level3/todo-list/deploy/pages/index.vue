<template>
  <div class="container">
    <div v-if="isLoggedIn" class="top-right">
      <button class="logout-button" @click="logout">Logout</button>
    </div>
    <div v-if="isLoggedIn">
      <h1>Your Todo Lists</h1>
      <button @click="toggleAddTodo">+ Add Todo</button>
      <div v-if="showAddForm">
        <input type="text" v-model="newTodo.title" placeholder="Title" required>
        <textarea v-model="newTodo.description" placeholder="Description" required></textarea>
        <input type="date" v-model="newTodo.dueDate">
        <button @click="addTodo">Submit</button>
      </div>
      <ul v-if="todoLists.length">
        <li v-for="item, idx in todoLists" :key="idx">
          <span :class="{ completed: item.is_completed }">{{ item.title }}: {{ item.description }}</span>
          <input type="checkbox" v-model="item.is_completed" @change="updateTodoStatus(item)">
          <!--
          under construction 
          <button @click="shareTodo"> Share </button>
          -->
        </li>
      </ul>
      <p v-else>No Todo Lists found.</p>
    </div>
    <div v-else>
      <h1>Welcome to Our Todo App</h1>
      <p>You are not logged in.</p>
      <button class="button" @click="navigateToLogin">Login</button>
      <button class="button" @click="navigateToSignup">Sign Up</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

const isLoggedIn = ref(false);
const todoLists = ref([]);
const router = useRouter();
const errorMessage = ref("");
const isLoading = ref(false);


onMounted(async () => {
  const token = localStorage.getItem('auth_token');
  if (token) {
    isLoggedIn.value = true;
    fetchTodolist(token);
  }
});

async function fetchTodolist(token) {
  isLoading.value = true;
  try {
    const response = await fetch('/api/todolist', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    if (response.ok) {
      todoLists.value = await response.json();
      todoLists.value.forEach(todo => {
      todo.is_completed = Boolean(todo.is_completed); 
    });
    } else {
      throw new Error('Failed to fetch todo lists');
    }
  } catch (error) {
    console.error('Error:', error);
    errorMessage.value = 'Error fetching todo lists: ' + error.message;
    router.push('/');
  } finally {
    isLoading.value = false;
  }
}
function logout() {
  localStorage.removeItem('auth_token');
  isLoggedIn.value = false;
  router.push('/');
}

function navigateToLogin() {
  router.push('/login');
}

function navigateToSignup() {
  router.push('/signup');
}
const showAddForm = ref(false);
const newTodo = ref({
  title: '',
  description: '',
  dueDate: ''
});

const toggleAddTodo = () => {
  showAddForm.value = !showAddForm.value;
  if (!showAddForm.value) {
    newTodo.value = { title: '', description: '', dueDate: '' };
  }
};

const addTodo = async () => {
  try {
    const data = JSON.stringify({
      title: newTodo.value.title,
      description: newTodo.value.description,
      dueDate: newTodo.value.dueDate || undefined
    });
    const token = localStorage.getItem('auth_token');
    if (!token) {
      throw new Error('login plz');
    }
    const response = await fetch('/api/todo', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: data,
    });
    if (!response.ok) {
      throw new Error('Failed to add todo');
    }
    toggleAddTodo();
    todoLists.value.push(JSON.parse(data));
  } catch (error) {
    console.error('Error adding todo:', error);
    alert('Error adding todo');
  }
}

async function shareTodo(todo) {
  try {
    const data = JSON.stringify(
      todo
    );
    const token = localStorage.getItem('auth_token');
    if (!token) {
      throw new Error('login plz');
    }
    const response = await fetch('/api/shareTodo', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: data,
    });
    if (!response.ok) {
      throw new Error('Failed to share api');
    }
  } catch (error) {
    console.error('Error share todo:', error);
    alert('Error share todo');
  }
}

async function updateTodoStatus(todo) {
  try {
    const data = JSON.stringify({
      id: todo.id,
      value: todo.is_completed,
    });
    const token = localStorage.getItem('auth_token');
    if (!token) {
      throw new Error('login plz');
    }
    const response = await fetch('/api/updateTodo', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: data,
    });
    if (!response.ok) {
      throw new Error('Failed to add todo');
    }
  } catch (error) {
    console.error('Error patching todo:', error);
    alert('Error patching todo');
  }
}
</script>


<style scoped>
.todo-list-container ul {
  list-style-type: none;
  padding: 0;
}

.todo-item {
  padding: 10px;
  border-bottom: 1px solid #ccc;
  display: flex;
  align-items: center;
}

.todo-item input[type="checkbox"] {
  margin-right: 10px;
}

.completed {
  text-decoration: line-through;
  color: #aaa;
}
</style>
