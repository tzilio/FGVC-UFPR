#!/bin/bash

# Array com os nomes das marcas, na ordem correspondente aos diretórios
marcas=("AGRALE" "AUDI" "BMW" "CHERY" "CHEVROLET" "CITROEN" "DODGE" "FIAT" "FORD" "HONDA"
        "HYUNDAI" "IVECO" "JAC" "JEEP" "KIA" "LAND-ROVER" "MARCOPOLO" "MERCEDES-BENZ" "MITSUBISHI"
        "NISSAN" "PEUGEOT" "RENAULT" "SCANIA" "SSANGYONG" "SUZUKI" "TOYOTA" "TROLLER" "VOLVO" "VW")

# Loop para renomear os diretórios de 0 a 28
for i in {0..28}; do
    if [ -d "$i" ]; then
        mv "$i" "${marcas[$i]}"
        echo "Diretório $i renomeado para ${marcas[$i]}"
    else
        echo "Diretório $i não encontrado!"
    fi
done

echo "Renomeação concluída."
