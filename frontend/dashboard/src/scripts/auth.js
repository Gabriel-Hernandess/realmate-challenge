export async function login(username, password) {
  const res = await fetch('http://localhost/auth/login/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password }),
    credentials: 'include'
  });

  if (!res.ok) throw new Error('Login failed');
  return res.json();
}

export async function logout() {
  await fetch('http://localhost/auth/logout/', {
    method: 'POST',
    credentials: 'include'
  });
}