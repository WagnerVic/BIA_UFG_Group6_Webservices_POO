// Função para carregar os usuários a partir do backend (JSON)
async function loadUsers() {
  try {
    const response = await fetch('/api/users');
    if (!response.ok) {
      throw new Error('Erro ao carregar os usuários');
    }
    const users = await response.json();
    return users;
  } catch (error) {
    console.error('Erro ao carregar os usuários:', error);
    return [];
  }
}

// Lógica de login
document.getElementById('loginForm').addEventListener('submit', async function(event) {
  event.preventDefault();

  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;

  const users = await loadUsers(); // Obter usuários do backend

  // Verificar se o nome de usuário e senha coincidem com algum usuário armazenado
  const user = users.find(user => user.username === username && user.password === password);

  if (user) {
    document.getElementById('errorMessage').style.display = 'none';
    alert('Login bem-sucedido!');

    // Armazenar os dados do usuário logado no localStorage
    localStorage.setItem('loggedInUser', JSON.stringify(user));

    // Redirecionar para a página inicial ou página específica dependendo do perfil
    if (user.profile === 2) {
      window.location.href = '/admin'; // Se for admin, redireciona para uma página de administração
    } else {
      window.location.href = '/user'; // Usuário comum é redirecionado para a página inicial
    }
  } else {
    document.getElementById('errorMessage').style.display = 'block';
  }
});

// Exibir o formulário de registro
document.getElementById('showRegisterForm').addEventListener('click', function(event) {
  event.preventDefault();
  window.location.href = '/register';
});

// Enviar o formulário de registro
document.getElementById('registerForm').addEventListener('submit', async function(event) {
  event.preventDefault();

  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;
  const confirmPassword = document.getElementById('confirmPassword').value;

  const users = await loadUsers(); // Obter usuários do backend

  // Verificar se o nome de usuário já existe
  const existingUser = users.find(user => user.username === username);

  if (existingUser) {
    alert("Nome de usuário já existe. Por favor, escolha outro.");
    return;
  }

  // Verificar se as senhas coincidem
  if (password !== confirmPassword) {
    alert("As senhas não coincidem.");
    return;
  }

  // Criar um novo usuário
  const newUser = { username, password, profile: 1 };  // Por padrão, o perfil é 'user'

  // Enviar o novo usuário para o backend
  try {
    const response = await fetch('/api/users', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(newUser),
    });

    if (!response.ok) {
      const error = await response.json();
      alert(error.error); // Exibe erro se o nome de usuário já existir
      return;
    }

    alert("Conta criada com sucesso!");
    window.location.href = '/login'; // Redirecionar para a página de login
  } catch (error) {
    console.error('Erro ao registrar o usuário:', error);
    alert('Erro ao criar a conta.');
  }
});
