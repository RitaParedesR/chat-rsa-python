# Chat Cifrado E2EE en Consola con Criptosistema RSA

> **Proyecto Integrador de Matemáticas Discretas** > *Escuela Superior Politécnica del Litoral (ESPOL)* > *Facultad de Ciencias Naturales y Matemáticas*

Prototipo de software orientado a procedimientos que implementa un **chat en consola (CLI)** con **cifrado de extremo a extremo (E2EE)** mediante el algoritmo asimétrico **RSA**, desarrollado desde cero en Python sin uso de librerías criptográficas externas.

---

## Características Principales

* **Criptografía RSA Desde Cero:** Implementación manual de la generación de primos, cálculo del totiente de Euler $\phi(n)$, Algoritmo de Euclides (MCD) y Algoritmo Extendido de Euclides para el inverso modular.
* **Arquitectura Cliente-Servidor:** Comunicación bidireccional basada en la capa de transporte TCP/IP utilizando la librería nativa `socket`.
* **Intercambio Automático de Claves (*Handshake*):** Al conectar, el servidor y el cliente generan sus llaves públicas/privadas e intercambian sus llaves públicas automáticamente usando `json`.
* **Confidencialidad Garantizada:** Las tramas que viajan por el socket contienen únicamente vectores de enteros resultantes de la exponenciación modular, impidiendo la lectura del mensaje a terceros no autorizados.


## Fundamentos Matemáticos Integrados

El proyecto demuestra empíricamente la aplicación de la **teoría de números** y la **aritmética modular**:

1. **Generación de Claves:**
   * Selección de dos primos aleatorios $p$ y $q$.
   * Módulo público: $n = p \cdot q$
   * Función Totiente de Euler: $\phi(n) = (p - 1) \cdot (q - 1)$
   * Exponente público $e$ tal que $\gcd(e, \phi(n)) = 1$.
   * Exponente privado $d$ tal que $d \cdot e \equiv 1 \pmod{\phi(n)}$ (calculado con Euclides Extendido).

2. **Cifrado:**
   $$C = M^e \pmod n$$

3. **Descifrado:**
   $$M = C^d \pmod n$$


## Estructura del Repositorio

```text
.
├── rsa_cifrado.py    # Módulo de funciones matemáticas y lógica RSA
├── servidor.py       # Socket servidor TCP e hilo de escucha/envío
├── cliente.py        # Socket cliente TCP e interfaz de chat
├── image_218530.png  # Captura de pantalla de la evidencia de ejecución
└── README.md         # Documentación del proyecto
```

---

## Requisitos e Instalación

### Pre-requisitos
* **Python 3.8+** instalado.
* No se requieren librerías de terceros (utiliza exclusivamente módulos nativos de Python: `socket`, `json`, `random`).

### Pasos de Ejecución

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/RitaParedesR/chat-rsa-python.git
   cd chat-rsa-python
   ```

2. **Iniciar el Servidor (Terminal 1):**
   Abre una terminal en la carpeta del proyecto y ejecuta:
   ```bash
   python servidor.py
   ```

3. **Iniciar el Cliente (Terminal 2):**
   Abre una segunda terminal en la misma carpeta y ejecuta:
   ```bash
   python cliente.py
   ```

4. **¡Chatear!** Al conectarse, ambos programas realizarán automáticamente el intercambio de claves públicas (*handshake*). Escribe `salir` en cualquiera de las terminales para finalizar la sesión de forma segura.


##  Autor
* **Paredes Robalino Rita** — [ritapare@espol.edu.ec](mailto:ritapare@espol.edu.ec)

**Docente:** Ph.D. Ebner Pineda Mogollón  
**Materia:** Matemáticas Discretas (Paralelo 5)  
**Guayaquil - Ecuador**
