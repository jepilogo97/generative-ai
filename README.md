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

![Imagen_](https://github.com/user-attachments/assets/1118ea75-2b94-4192-bf97-d3ed4f5a29bb)

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


## Fase 2 – Evaluación de Fortalezas, Limitaciones y Riesgos Éticos

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