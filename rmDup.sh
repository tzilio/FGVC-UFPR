#!/bin/bash

declare -A placas_encontradas

# Percorre todas as imagens no diretório e subdiretórios
find . -type f -name "*.jpg" | while read -r arquivo; do
    # Extrai a placa do nome do arquivo
    placa=$(echo "$arquivo" | awk -F '-' '{print $2}')

    # Verifica se a placa já foi encontrada
    if [[ -n "${placas_encontradas[$placa]}" ]]; then
        # Se a placa já foi encontrada, remove o arquivo duplicado
        echo "Removendo duplicata: $arquivo"
        rm "$arquivo"
    else
        # Caso contrário, armazena a placa no array
        placas_encontradas[$placa]=1
    fi
done
