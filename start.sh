#!/bin/bash

# FinanceControl - Start Script
# Script para iniciar a aplicação Flask facilmente

echo "🚀 Iniciando FinanceControl..."
echo ""

# Verificar se o venv existe
if [ ! -d "venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv venv
fi

# Ativar venv
source venv/bin/activate

# Instalar dependências (se houver mudanças)
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt > /dev/null 2>&1
fi

echo "✅ Ambiente pronto!"
echo ""
echo "💰 FinanceControl"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🌐 Acesse: http://localhost:5000"
echo "⚙️  Debug: ATIVADO"
echo ""
echo "Pressione CTRL+C para parar o servidor"
echo ""

# Executar a aplicação
python app.py
