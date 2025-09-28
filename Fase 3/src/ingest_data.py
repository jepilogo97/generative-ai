import json
import faiss
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer

MODEL_EMBED = "all-MiniLM-L6-v2"

def build_faiss_index():
    """
    Lee pedidos.json, crea embeddings descriptivos para cada pedido
    incluyendo todos los campos relevantes, y genera el índice FAISS.
    """
    script_dir = Path(__file__).resolve().parent
    data_dir = script_dir.parent / "data"
    data_dir.mkdir(exist_ok=True)

    index_file = data_dir / "faiss_index.bin"
    metadata_file = data_dir / "metadata.json"
    pedidos_file = data_dir / "pedidos.json"

    print("🔄 Cargando modelo de embeddings...")
    model = SentenceTransformer(MODEL_EMBED)

    print("🔄 Leyendo datos de pedidos...")
    with open(pedidos_file, "r", encoding="utf-8") as f:
        pedidos = json.load(f)

    textos = []
    for p in pedidos:
        # Construir descripción de productos
        productos_txt = " | ".join(
            f"{prod.get('nombre','')} "
            f"({prod.get('categoria','')}, "
            f"dev_aceptada: {prod.get('dev_aceptada', False)})"
            for prod in p.get("productos", [])
        )

        # Crear texto con TODOS los campos relevantes de la estructura
        texto = (
            f"Pedido {p.get('tracking_number','')} "
            f"Estado: {p.get('estado','')} "
            f"Fecha estimada: {p.get('fecha_estimada','')} "
            f"Fecha entrega real: {p.get('fecha_entrega_real','')} "
            f"Destino: {p.get('destino','')} "
            f"Transportadora: {p.get('transportadora','')} "
            f"Enlace de rastreo: {p.get('enlace_rastreo','')} "
            f"Cliente: {p.get('cliente','')} "
            f"Peso (kg): {p.get('peso_kg','')} "
            f"Valor (USD): {p.get('valor_usd','')} "
            f"Motivo retraso: {p.get('motivo_retraso','')} "
            f"Motivo cancelación: {p.get('motivo_cancelacion','')} "
            f"Punto de retiro: {p.get('punto_retiro','')} "
            f"Productos: {productos_txt}"
        ).replace("\n", " ").strip()

        textos.append(texto)

    if not textos:
        raise ValueError("No se encontraron pedidos para indexar.")

    print(f"🔄 Generando embeddings para {len(textos)} pedidos...")
    embeddings = model.encode(textos, convert_to_numpy=True, normalize_embeddings=True)
    embeddings = embeddings.astype("float32")

    # Crear y guardar índice FAISS
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    faiss.write_index(index, str(index_file))

    # Guardar metadatos tal cual
    with open(metadata_file, "w", encoding="utf-8") as f:
        json.dump(pedidos, f, ensure_ascii=False, indent=2)

    print(f"✅ FAISS index creado con {len(textos)} registros.")
    print(f"   Índice guardado en: {index_file}")
    print(f"   Metadatos guardados en: {metadata_file}")


if __name__ == "__main__":
    build_faiss_index()
    print("✅ FAISS index creado.")
