// Função para carregar os usuários a partir do backend (Exemplo fictício de carregamento)
async function loadUsers() {
  try {
    // Aqui estamos simulando a resposta do backend, já que você forneceu os dados diretamente
    const users = [
      { "username": "Lola", "password": "1", "profile": 2 },
      { "username": "iAmAUser", "password": "verysafepass", "profile": 1 },
      { "username": "1", "password": "1", "profile": 1 }
    ];
    return users;
  } catch (error) {
    console.error('Erro ao carregar os usuários:', error);
    return [];
  }
}

// Função para salvar os usuários no backend (simulando a persistência)
async function saveUsers(users) {
  try {
    // Simulando o envio dos dados para o backend
    console.log("Usuários salvos:", users);
  } catch (error) {
    console.error('Erro ao salvar os usuários:', error);
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

    // Definir uma constante para o usuário logado
    const loggedInUser = JSON.parse(localStorage.getItem('loggedInUser'));

    // Exemplo de como usar o loggedInUser constante
    console.log('Usuário logado:', loggedInUser);

    // Redirecionar para a página inicial ou página específica dependendo do perfil
    if (loggedInUser.profile === 2) {
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

  // Adicionar o novo usuário com um nível de perfil
  const profile = 1; // Por padrão, o usuário será um 'user'
  const newUser = { username, password, profile };
  users.push(newUser);

  // Salvar os usuários no backend
  await saveUsers(users);

  alert("Conta criada com sucesso!");
  window.location.href = '/login'; // Redirecionar para a página de login
});
