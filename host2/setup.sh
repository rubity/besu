#!/bin/bash

set -e  # Para encerrar o script em caso de erro

echo "Atualizando lista de pacotes..."
sudo apt update -y
sudo apt upgrade -y

# Instalar dependências básicas
echo "Instalando dependências básicas..."
sudo apt install -y curl ca-certificates gnupg lsb-release software-properties-common

# ------------------------
# Instalação do Docker
# ------------------------
install_docker() {
	if ! command -v docker &> /dev/null; then
    	echo "Instalando Docker..."
    	sudo apt remove -y docker docker-engine docker.io containerd runc || true
    	sudo mkdir -m 0755 -p /etc/apt/keyrings
    	curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo tee /etc/apt/keyrings/docker.asc > /dev/null
    	echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    	sudo apt update -y
    	sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    	sudo systemctl enable --now docker
    	sudo usermod -aG docker $USER
    	echo "Docker instalado com sucesso!"
	else
    	echo "Docker já está instalado, verificando atualizações..."
    	sudo apt install -y --only-upgrade docker-ce docker-ce-cli containerd.io
	fi
}

# ------------------------
# Instalação do Docker Compose
# ------------------------
install_docker_compose() {
	echo "Verificando Docker Compose..."
	if ! command -v docker compose &> /dev/null; then
    	echo "Instalando Docker Compose..."
    	sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    	sudo chmod +x /usr/local/bin/docker-compose
    	sudo ln -sf /usr/local/bin/docker-compose /usr/bin/docker-compose
    	echo "Docker Compose instalado com sucesso!"
	else
    	echo "Docker Compose já está instalado!"
	fi
}

# ------------------------
# Instalação do NodeJS (Última versão LTS)
# ------------------------
install_nodejs() {
	echo "Instalando NodeJS (versão LTS mais recente)..."
	curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
	sudo apt install -y nodejs
	echo "NodeJS instalado com sucesso! Versão: $(node -v)"
}

# Executando as funções
install_docker
install_docker_compose
install_nodejs

# Copiar Repositorio da Rede
echo "📌 Copiando o Repositorio da Rede Besu..."
#sudo git clone https://github.com/MiguelEuripedes/besu-quickstarter-modified

# Mensagem final
echo "✅ Configuração finalizada! Todos os aplicativos foram instalados com sucesso!"
echo "ℹ️ Reinicie seu terminal para aplicar as permissões do Docker."

exit 0
