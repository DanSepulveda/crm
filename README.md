# 📌 Sistema de Gestión de Clientes

Aplicación de escritorio desarrollada en **Python** utilizando **Tkinter** para la gestión de clientes.  
Permite crear, editar, eliminar y visualizar distintos tipos de clientes, almacenando la información en formato JSON.

---

## 🚀 Funcionalidades

- ✅ Crear clientes
- ✅ Editar clientes existentes
- ✅ Eliminar clientes
- ✅ Búsqueda y filtrado
- ✅ Soporte para múltiples tipos de cliente:
  - Regular
  - Premium
  - Corporativo
- ✅ Registro de logs de operaciones
- ✅ Persistencia de datos en archivo `clientes.json`

---

## 🧱 Arquitectura

El proyecto sigue una separación por capas:

- **Vista (Tkinter)** → Interfaz gráfica
- **Servicio** → Lógica de negocio
- **Repositorio** → Acceso y persistencia de datos
- **Dominio** → Modelos (`Cliente`, `Direccion`, etc.)

Se aplica separación de responsabilidades para mantener el código organizado y mantenible.

---

## 🛠 Tecnologías utilizadas

- Python 3
- Tkinter (ttk)
- JSON para almacenamiento de datos
- Logging para registro de eventos

---

## ▶ Cómo ejecutar el proyecto

1. Clonar el repositorio
2. Ejecutar:

```bash
python main.py
```
