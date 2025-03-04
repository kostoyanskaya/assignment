const API_BASE_URL = 'http://127.0.0.1:8000';

async function login() {
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;

  try {
    const response = await fetch(`${API_BASE_URL}/auth/token/login/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    });

    if (!response.ok) {
      throw new Error('Ошибка при входе');
    }

    const data = await response.json();
    localStorage.setItem('token', data.auth_token); // Обратите внимание на data.auth_token
    window.location.href = '/';
  } catch (error) {
    console.error('Ошибка при входе:', error);
    document.getElementById('auth-error').textContent = 'Неверное имя пользователя или пароль';
  }
}