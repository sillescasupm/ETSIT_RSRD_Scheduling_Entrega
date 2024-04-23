# Scheduling de Recursos en Comunicaciones

## Descripción

Este proyecto consiste en un programa Python para realizar el scheduling de recursos en sistemas de comunicaciones. El programa implementa varios algoritmos de scheduling, incluyendo MAX C/I, que permite maximizar la capacidad de transmisión para cada usuario, y Proportional Fair, que distribuye el ancho de banda de manera proporcional entre los usuarios.

El programa define dos clases principales: `Zone` y `Scenario`. La clase `Zone` representa una zona de comunicación con atributos como el nombre, el número de usuarios, la tasa de bits por hercio (bps/Hz), la tasa pico de transmisión (r_peak) y la tasa mínima garantizada (r_sla). La clase `Scenario` maneja el escenario de comunicación global, incluyendo el ancho de banda total disponible y las zonas de comunicación involucradas.

## Funcionalidades Implementadas

- **MAX C/I:** El algoritmo de Max Capacity per User (MAX C/I) busca maximizar la relación señal a interferencia más ruido (SINR) para cada usuario, asegurando una alta capacidad de transmisión.
- **MAX C/I con MinRate:** Se ha implementado una variante de MAX C/I que garantiza una tasa mínima de transmisión (MinRate) para todos los usuarios.
- **Proportional Fair:** Este algoritmo distribuye el ancho de banda disponible de manera proporcional entre los usuarios, promoviendo la equidad en el acceso a los recursos.

## Ejecución del Programa

Para ejecutar el programa, simplemente ejecuta el script `main.py`. Este script prueba las funcionalidades implementadas en el programa, mostrando los resultados de cada algoritmo de scheduling para un escenario predefinido.

## Dependencias

El programa requiere Python 3 para ejecutarse. No tiene dependencias externas adicionales.

## Ejemplo de Uso

```python
python main.py
