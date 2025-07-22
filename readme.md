# EIRI - Virtual Assistant with Python Command Execution

![Badge](https://img.shields.io/badge/License-MIT-blue)
![Badge](https://img.shields.io/badge/Ollama-Compatible-brightgreen)
![Badge](https://img.shields.io/badge/PlatformIO-Supported-orange)

**EIRI** es un asistente virtual diseñado para ejecutar comandos de Python con capacidades avanzadas de contexto, evaluación, coherencia y memoria. Permite la ejecución inteligente de funciones, manteniendo una conversación fluida y relevante con el usuario.

---

## 🚀 Características

- **🧠 Evaluación contextual de funciones**: Utiliza el contexto de interacciones anteriores para evaluar funciones con mayor precisión.
- **✅ Retroalimentación de ejecución**: Informa si una función se ejecutó correctamente o si hubo un error, mostrando el resultado correspondiente.
- **🕵️‍♂️ Verificación de coherencia**: Antes de ejecutar cualquier función, valida si la solicitud del usuario es coherente.
- **🧾 Gestión de memoria**: Mantiene un historial de las últimas 5-7 interacciones relacionadas con funciones para conservar el contexto.
- **🧪 Evaluación de comandos**: Mejora la interpretación de órdenes evitando salidas inesperadas como respuestas ambiguas.

---

## 🤖 Modelos Compatibles

### ✅ Probado y Funcional
- **phi3**
- **llama3**

### ⚠️ Funcional con Errores
- **mistral**: Problemas al generar argumentos adecuados.
- **wizardlm2**: A veces no detecta cuándo se requiere una función.
- **dolphin-mistral**: Ocasionalmente elige la función incorrecta.
- **orca-mini**: Falla al evaluar si se debe ejecutar una función.

---

## 📄 Licencia

Este proyecto está bajo la **Licencia MIT**. Consulta el archivo [LICENSE](./LICENSE) para más información.

---

## ✨ Créditos

Desarrollado por [senchpimy](https://github.com/senchpimy)
