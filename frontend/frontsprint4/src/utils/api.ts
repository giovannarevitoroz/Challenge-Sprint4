// src/utils/api.ts

export async function getUsuarios() {
    const response = await fetch('http://localhost:8080/sprint4-java/rest/usuario');
    if (!response.ok) {
      throw new Error('Falha ao buscar usuários');
    }
    return response.json();
  }
  