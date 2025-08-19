<template>
  <div class="container">
    <h1>Login</h1>
    <form @submit.prevent="handleLogin">
      <div>
        <label for="email">Email:</label>
        <input type="email" id="email" v-model="loginForm.email" required>
      </div>
      <div>
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="loginForm.password" required>
      </div>
      <button class="button" type="submit">Log In</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const loginForm = ref({
  email: '',
  password: ''
});

const router = useRouter();
const errorMessage = ref("");

const handleLogin = async () => {
  try {
    const response = await fetch('/api/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(loginForm.value)
    });
    const data = await response.json();
    if (response.ok) {
      localStorage.setItem('auth_token', data.token);
      router.push('/');
    } else {
      loginError.value = true;
      errorMessage.value = data.message || 'Login failed. Please try again.';
    }
  } catch (error) {
    loginError.value = true;
    errorMessage.value = 'An error occurred during login.';
    console.error('Error logging in:', error);
  }
};
</script>

<style scoped></style>