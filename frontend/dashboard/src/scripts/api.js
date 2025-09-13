export async function fetchConversations() {
  const res = await fetch('http://localhost/conversations/', {
    credentials: 'include'
  });
  if (!res.ok) throw new Error('Failed to fetch conversations');
  return res.json();
}