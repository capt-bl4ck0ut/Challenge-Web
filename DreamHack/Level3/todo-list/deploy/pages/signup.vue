<template>
    <div class="container">
      <h1>Sign Up</h1>
      <form @submit.prevent="handleSubmit">
        <div>
          <label for="username">Username:</label>
          <input type="text" id="username" v-model="form.username" required>
        </div>
        <div>
          <label for="email">Email:</label>
          <input type="email" id="email" v-model="form.email" required>
        </div>
        <div>
          <label for="password">Password:</label>
          <input type="password" id="password" v-model="form.password" required>
        </div>
        <button type="submit">Sign Up</button>
      </form>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import { useRouter } from 'vue-router';
  
  const form = ref({
    username: '',
    email: '',
    password: ''
  });
  
  const router = useRouter();
  
  async function handleSubmit() {
    try {
      const response = await fetch('/api/signup', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(form.value)
      });
      const data = await response.json();
      if (response.ok) {
        alert('Signup successful!');
        router.push('/login'); 
      } else {
        alert(data.message);
      }
    } catch (error) {
      console.error('Error signing up:', error);
      alert('An error occurred while signing up.');
    }
  }
  </script>
  