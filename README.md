# Taller AI Generativa
Este repositorio contiene el material y el código del taller “Optimización de la Atención al Cliente en E-commerce con IA Generativa”, basado en el caso de estudio de la empresa ficticia "EcoMarket".


# Fase 1 – Selección y Justificación del Modelo de IA

## 1️⃣ Tipo de modelo propuesto
Optaría por un **LLM de propósito general** , en este caso el *Llama 3* combinado con un enfoque de **Retrieval-Augmented Generation (RAG)**.

- **Motivo principal:** La mayoría de las consultas (≈ 80 %) son repetitivas y dependen de información actualizada del negocio (estado de pedidos, políticas de devolución, catálogo).  
  Un RAG permite que el modelo base no requiera reentrenamiento cada vez que cambian los datos: solo necesita conectarse a una base de conocimiento dinámica.


## 2️⃣ Por qué la elección del modelo
- **Precisión y fluidez:** Un LLM grande ofrece lenguaje natural y tono empático para responder en múltiples canales (chat, email, redes sociales).
- **Costo / eficiencia:** En lugar de un *fine-tuned* propietario —que implicaría entrenamiento continuo y costo elevado— el enfoque RAG permite usar el modelo tal cual, complementado con datos internos indexados.
- **Escalabilidad:** El mismo modelo puede atender picos de miles de consultas diarias mediante *autoscaling* en la nube.
- **Privacidad:** Es posible tener un control total de los datos al usar con una infraestructura propia en la nube.


## 3️⃣ Arquitectura propuesta  

<img src="https://github.com/user-attachments/assets/125198ab-9ede-4245-86e2-b36eff960e99" width="450" alt="Diagrama del flujo" />

## ⚙️ Tecnologías Seleccionadas y Justificación

### 🧩 Gateway + API
El **gateway** gestiona el tráfico y la seguridad; la **API (FastAPI)** recibe la solicitud y la pasa al orquestador.

- Esta separación permite **escalar** y **asegurar** el sistema, dado el rápido crecimuiento se recomienda separar estos roles.

### 🔗 LangChain + FastAPI
Combina la **orquestación de flujos de IA** de **LangChain** con la **velocidad y facilidad de despliegue** de **FastAPI**, ofreciendo una API robusta, escalable y de alta disponibilidad para integrar el modelo con los distintos canales de comunicación.

### 🗂️ FAISS
Librería **open source** optimizada para **búsquedas vectoriales rápidas**.  
Permite mantener **control total de los datos** y **reducir costos**, ideal para gestionar el índice semántico de productos y pedidos sin depender de servicios de terceros.

### 🤖 Llama 3
Modelo de lenguaje **open source** de alto rendimiento que brinda **privacidad y personalización** al ejecutarse en una nube privada.  
Ofrece **calidad de generación cercana a GPT-4** con la flexibilidad de *fine-tuning* y **costos predecibles**.


- **Integración con base de datos:**  
  - Catálogo de productos, información de envíos y estados de pedido se almacenan en una base de datos relacional/NoSQL y se indexan en un motor vectorial para consultas en tiempo real.  
  - El modelo consulta estos datos mediante RAG antes de redactar la respuesta.
- **Modo de operación:**  
  - Para preguntas de estado de pedido, una capa de lógica de negocio valida identidad y obtiene datos exactos.  
  - Para consultas complejas (20 %), el sistema deriva automáticamente a un agente humano, entregando el contexto de la conversación.


## 4️⃣ Justificación Final

- **Costo:**  
  Uso de un **LLM open source (Llama 3)** junto con un índice vectorial **FAISS** permite **evitar tarifas por token** y mantener **costos predecibles**.  
  Se paga únicamente por la infraestructura en la nube, que puede dimensionarse según la demanda.

- **Escalabilidad:**  
  La arquitectura combina **Gateway + API (FastAPI)** con un orquestador en **LangChain**, facilitando el *autoscaling* en la nube.  
  Esto permite manejar miles de consultas simultáneas, con **balanceo de carga** y **cacheo de respuestas frecuentes** para optimizar recursos.

- **Mantenibilidad:**  
  La base de conocimiento se actualiza dinámicamente en **FAISS**, sin necesidad de reentrenar el modelo.  
  La separación de capas (Gateway, API, Orquestador y Vector DB) simplifica actualizaciones y despliegues continuos.

- **Privacidad y Control de Datos:**  
  **Llama 3** puede ejecutarse en una nube privada, asegurando que las conversaciones y datos de clientes permanezcan bajo control total, clave para cumplir regulaciones.

- **Calidad de Respuesta:**  
  **Llama 3**, integrado con LangChain, ofrece **lenguaje natural, empatía y soporte multicanal**, garantizando interacciones de alta calidad.  
  Además, el orquestador identifica consultas complejas y **deriva automáticamente a un agente humano** con el contexto completo para una atención sin fricciones.

---


# Fase 2 – Evaluación de Fortalezas, Limitaciones y Riesgos Éticos

### 💪 Fortalezas
- **Reducción del tiempo de respuesta:**  
  El sistema puede responder en segundos, disminuyendo el promedio de 24 horas a casi tiempo real.
- **Disponibilidad 24/7:**  
  La arquitectura en la nube permite atender consultas sin interrupciones, incluso en picos de demanda.
- **Cobertura de consultas repetitivas (~80 %):**  
  El orquestador con RAG (LangChain + FAISS) recupera información precisa del catálogo y pedidos de EcoMarket.
- **Escalabilidad y costos controlados:**  
  FAISS y Llama 3 autohospedado ofrecen independencia de tarifas por token y facilitan el crecimiento según demanda.
- **Privacidad y control de datos:**  
  Al ejecutar Llama 3 en infraestructura privada, EcoMarket mantiene la propiedad de los datos sensibles.

### ⚠️ Limitaciones
- **Casos complejos (~20 %):**  
  Requieren empatía y juicio humano (quejas graves, conflictos de reembolso). 
- **Dependencia de la base de conocimiento:**  
  Si FAISS contiene información desactualizada o errónea, el modelo puede devolver respuestas incorrectas.
- **Mantenimiento de infraestructura:**  
  Ejecutar Llama 3 en la nube implica monitoreo de GPUs, actualizaciones de seguridad y optimización de costos.
- **Idioma y matices culturales:**  
  Aunque Llama 3 es multilingüe, podría cometer errores sutiles en expresiones locales o tonos específicos.

### 🛑 Riesgos Éticos

1. **Alucinaciones:**  
   El modelo podría inventar información sobre pedidos o características de productos.  
   - *Mitigación:* Validar datos críticos (estado de pedido, precios) con reglas de negocio antes de enviar la respuesta.

2. **Sesgo:**  
   Los datos de entrenamiento pueden contener sesgos que generen respuestas preferenciales o discriminatorias.  
   - *Mitigación:* Monitoreo constante, pruebas de equidad y ajuste de *prompts*.

3. **Privacidad de Datos:**  
   El sistema maneja direcciones, historial de compras y datos personales.  
   - *Mitigación:* Cifrado en tránsito y reposo, anonimización de logs, control estricto de acceso, y no-retención en servicios externos.

4. **Impacto Laboral:**  
   La automatización podría reducir la necesidad de agentes humanos.  
   - *Mitigación:* Enfocar el proyecto en **empoderar** a los agentes, delegando en la IA las tareas repetitivas y permitiendo que el personal se centre en casos complejos o de alto valor.

---

**Conclusión:**  
La solución basada en **LangChain + FastAPI, FAISS y Llama 3** es potente para reducir tiempos de respuesta y manejar la mayoría de las consultas.  
Sin embargo, requiere una estrategia clara de **supervisión humana, gobernanza de datos y gestión del cambio** para mitigar riesgos éticos y preservar la calidad del servicio.


# Fase 3 · Sistema de consulta de pedidos

## Resumen
Aplicación web con asistente conversacional para consultar estados de pedidos. Combina:
- Interfaz de chat en Streamlit para clientes.
- Motor conversacional que usa búsqueda vectorial (FAISS + Sentence Transformers) y generación con Llama 3 vía Ollama.

## Arquitectura

| Componente | Descripción |
|------------|-------------|
| `start.py` | Orquesta la ejecución local: verifica Docker, reconstruye (si corresponde) la imagen `pedidos-app` y lanza el contenedor con los puertos 8501 (Streamlit) y 11434 (Ollama). |
| `check_docker.py` | Diagnóstico independiente: valida instalación/estado de Docker y disponibilidad de archivos clave; puede ejecutar `docker build --dry-run`. |
| `Dockerfile` | Imagen basada en `python:3.11-slim`; instala compiladores/bibliotecas para FAISS y NumPy, añade Ollama, prepara dependencias y configura `entrypoint.sh`. |
| `entrypoint.sh` | Dentro del contenedor: inicia Ollama, espera disponibilidad, descarga el modelo `llama3` si falta y lanza la app de Streamlit. |
| `requirements.txt` | Dependencias fijadas para FAISS, Sentence Transformers, Ollama, Streamlit y utilidades de Hugging Face. |
| `src/streamlit_app.py` | UI del chat: administra estado en `st.session_state`, detecta números de seguimiento, prepara contexto y llama a `ollama.chat` para responder. |
| `src/settings.toml` | Configuración del modelo (nombre, temperatura) y prompts/instrucciones para diferenciar consultas de seguimiento y devoluciones. |
| `src/ingest_data.py` | Pipeline de indexación: lee `data/pedidos.json`, genera descripciones enriquecidas, calcula embeddings (`all-MiniLM-L6-v2`), crea el índice FAISS y persiste metadatos. |
| `data/pedidos.json` | 30 pedidos de ejemplo con estado, fechas, destino, transportista, enlaces, productos y políticas de devolución. |

## Flujo operativo

1. Ejecutar `python start.py` (o pasos manuales equivalentes).
2. El script valida Docker y reconstruye/lanzar el contenedor `pedidos-app`.
3. El contenedor inicia Ollama, garantiza la disponibilidad del modelo `llama3` y arranca la aplicación Streamlit en `http://localhost:8501`.
4. La UI permite consultar pedidos; al detectar un número válido, busca contexto en el índice FAISS y genera respuestas empáticas y estructuradas según `settings.toml`.

## Datos y modelo

- **Datos:** `data/pedidos.json` alimenta la indexación y la UI.
- **Modelo conversacional:** Llama 3 servido por Ollama, configurado mediante `settings.toml`.

## Prompts utilizados

[prompts]

# -------------------------------------------------------------------
# Rol del modelo
# -------------------------------------------------------------------
role_prompt = """
Eres un agente virtual de servicio al cliente altamente capacitado,
especializado en seguimiento de pedidos y gestión de devoluciones.

Tu objetivo es brindar una experiencia de atención confiable y empática:

- Lee cuidadosamente la información del pedido y su lista de productos.
- Proporciona detalles claros y completos: número de seguimiento, estado actual,
  fecha estimada o real de entrega, destino, transportadora y enlace de rastreo.
- Explica cualquier incidencia (retrasos, cancelaciones, aduanas, etc.) con un
  tono profesional, cercano y comprensible.
- **Jamás inventes datos**: usa únicamente la información provista.
- **No inventes nombres de clientes ni de productos.**
  - Si no se proporciona el nombre del cliente, usa un saludo neutro.
  - Para los productos, menciona solo los nombres tal como aparezcan en la información del pedido,
    sin abreviaciones ni creaciones propias.
- Mantén siempre un lenguaje amable, natural y cordial, evitando tecnicismos innecesarios.
- Adecúa la longitud del mensaje: breve y directo, pero con la información completa.
- Si la consulta no es clara, pide amablemente una aclaración.
"""

# -------------------------------------------------------------------
# Instrucciones principales
# -------------------------------------------------------------------
instruction_prompt = """
Analiza el contenido comprendido entre >>>>>CONTENIDO<<<<<.

El usuario puede:
1) Consultar el estado de un pedido.
2) Solicitar información sobre la devolución de productos.

Debes:

1. Detectar con precisión si la intención principal del usuario es:
   a) Conocer el estado de un pedido, o
   b) Obtener información sobre la devolución de productos.

2. Para **estado de pedido**:
   - Saluda de forma personalizada solo si el nombre del cliente está explícitamente disponible;
     de lo contrario, usa un saludo neutro (por ejemplo, "¡Hola!").
   - Informa de manera clara el número de seguimiento, estado actual,
     fecha estimada o real de entrega, destino, transportadora y, si existe,
     el enlace de rastreo.
   - Si hay retrasos, explica brevemente el motivo y ofrece disculpas empáticas.
   - Cierra con un mensaje de agradecimiento u ofrecimiento de ayuda adicional.

3. Para **devolución de productos**:
   - Saluda cordialmente, sin inventar nombre del cliente.
   - Confirma el número de seguimiento.
   - Revisa cada producto y menciona **exactamente** el nombre provisto en la información del pedido,
     indicando si la devolución está permitida o no.  
     En caso de negativa, explica el motivo (ej.: perecedero, higiene, política de devolución).
   - Finaliza con una breve orientación sobre los siguientes pasos
     (por ejemplo, cómo iniciar el trámite de devolución de los productos aceptados).

4. Si el pedido no existe o el número de seguimiento no se encuentra:
   - Responde con empatía y explica que no se halló información.
   - Invita a verificar el número o proporcionar más datos.

5. Estilo de respuesta:
   - Usa un lenguaje conversacional, cálido y profesional.
   - No entregues la respuesta en JSON ni en estructuras de datos.
   - Mantén la coherencia gramatical y un flujo natural,
     como si fueras un agente humano.
   - **Nunca infieras ni generes nombres de personas o productos que no aparezcan
     de forma explícita en los datos.**

6. Si el usuario envía varias preguntas (seguimiento y devolución a la vez):
   - Contesta de forma ordenada, cubriendo ambos temas en un solo mensaje,
     manteniendo claridad y cortesía.

Recuerda: la respuesta final debe ser un **mensaje fluido y natural**,
sin claves ni formato técnico y respetando los nombres exactos provistos.
"""

# -------------------------------------------------------------------
# Ejemplo de seguimiento (positivo)
# -------------------------------------------------------------------
positive_example = """
[Cliente] 2025-09-20: Hola, quiero saber el estado de mi pedido 20002.
[Agente]  2025-09-20: ¡Hola! Con gusto te ayudo. El pedido 20002 fue entregado
el 22 de septiembre de 2025 en Medellín, Colombia por FedEx.
Puedes ver el detalle en: https://www.fedex.com/fedextrack/?trknbr=20002.
¡Gracias por tu compra y que disfrutes tu producto!
"""

# -------------------------------------------------------------------
# Ejemplo de devolución (mixta)
# -------------------------------------------------------------------
return_example = """
[Cliente] 2025-10-01: Quiero devolver los productos del pedido 20004.
[Agente]  2025-10-01: Claro, ya revisé el pedido 20004. El "Yogur griego"
no puede devolverse porque es un alimento perecedero.
Si tienes más productos que desees devolver y cumplen las políticas,
con gusto te ayudo a iniciar el proceso. Gracias por tu comprensión.
"""

# -------------------------------------------------------------------
# Ejemplo de seguimiento con retraso
# -------------------------------------------------------------------
delay_example = """
[Cliente] 2025-10-05: Buen día, ¿qué pasa con mi pedido 30007?
[Agente]  2025-10-05: ¡Hola! Revisé el pedido 30007 y actualmente se encuentra
en tránsito con la transportadora DHL. La entrega estimada era el 4 de octubre,
pero se retrasó por condiciones climáticas en la ruta.
La nueva fecha estimada de entrega es el 7 de octubre de 2025.
Te pedimos disculpas por el inconveniente y agradecemos tu paciencia.
Puedes hacer seguimiento aquí: https://www.dhl.com/track?num=30007.
"""

# -------------------------------------------------------------------
# Ejemplo de pedido no encontrado
# -------------------------------------------------------------------
not_found_example = """
[Cliente] 2025-10-08: Necesito saber el estado del pedido 99999.
[Agente]  2025-10-08: Hola, intenté ubicar el pedido 99999, pero no encontré
información en nuestro sistema. Por favor verifica que el número de seguimiento
sea correcto o compárteme más detalles para ayudarte mejor.
"""

# -------------------------------------------------------------------
# Ejemplo de devolución múltiple
# -------------------------------------------------------------------
multi_return_example = """
[Cliente] 2025-10-10: Quiero devolver los artículos del pedido 45001.
[Agente]  2025-10-10: Con gusto. Para el pedido 45001:
- El "Pantalón de lino azul" puede devolverse hasta el 20 de octubre de 2025.
- La "Camiseta blanca algodón" también es aceptada para devolución.
- El "Set de velas aromáticas" no puede devolverse por política de productos
  frágiles y abiertos.
Si deseas continuar, puedo enviarte las instrucciones para devolver
los productos aceptados.
"""

# -------------------------------------------------------------------
# Ejemplo de consulta combinada (seguimiento + devolución)
# -------------------------------------------------------------------
combined_example = """
[Cliente] 2025-10-12: Hola, quiero saber si ya llegó mi pedido 50123 y
también si puedo devolver el "Paraguas rojo" de ese pedido.
[Agente]  2025-10-12: ¡Hola! El pedido 50123 fue entregado el 11 de octubre
de 2025 en Bogotá, Colombia por Servientrega.
En cuanto a la devolución, el "Paraguas rojo" puede devolverse
hasta el 25 de octubre de 2025.
Si deseas iniciar el proceso, te envío las indicaciones.
"""


## Automatización y pruebas

- Scripts de verificación (`start.py`, `check_docker.py`) manejan reconstrucciones, detección de puertos ocupados y fallos comunes.
- La validación se realiza mediante inspección estática y pruebas manuales de la app.

## Ejemplos de pruebas

<img width="793" height="556" alt="image" src="https://github.com/user-attachments/assets/3dc7d6f1-cf9c-4a8e-8116-cec021215d7a" />

<img width="712" height="537" alt="image" src="https://github.com/user-attachments/assets/0fd99756-93b5-48da-9e67-a085eed37d8c" />

<img width="807" height="513" alt="image" src="https://github.com/user-attachments/assets/5adc0c9a-ee80-4034-b72a-9e6103e87a1f" />



