import os
import re
import math
import numpy as np
from unidecode import unidecode
from collections import Counter

#  Constantes y Configuraciones

# Ruta a la base de conocimiento
RUTA_DATASET = "dataset" 

# Numero de vecinos para votacion
K_VECINOS = 5 

# Stopwords en inglés
STOPWORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", 
    "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being", 
    "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't", 
    "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during", 
    "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", 
    "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", 
    "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", 
    "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", 
    "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself", 
    "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought", 
    "our", "ours", "ourselves", "out", "over", "own", "same", "shan't", "she", 
    "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such", 
    "than", "that", "that's", "the", "their", "theirs", "them", "themselves", 
    "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", 
    "they've", "this", "those", "through", "to", "too", "under", "until", "up", 
    "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were", 
    "weren't", "what", "what's", "when", "when's", "where", "where's", "which", 
    "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would", 
    "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours", 
    "yourself", "yourselves"
}

# 2) Funcion de Carga de Datos 

def cargar_documentos_desde_disco(ruta_dataset):
    documentos = []
    print(f"Cargando documentos desde '{ruta_dataset}'...")
    try:
        for categoria in os.listdir(ruta_dataset):
            categoria_path = os.path.join(ruta_dataset, categoria)
            if os.path.isdir(categoria_path):
                for filename in os.listdir(categoria_path):
                    file_path = os.path.join(categoria_path, filename)
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            texto = f.read()
                            documentos.append((categoria, texto))
                    except Exception as e:
                        print(f"  [!] Error leyendo {file_path}: {e}")
    except FileNotFoundError:
        print(f"  [ERROR] Directorio no encontrado: '{ ruta_dataset}'")
        return None
    
    print(f"Se cargaron {len(documentos)} documentos.")
    return documentos

# 3) Funcion de Preprocesamiento de Texto

def preprocesar_texto(texto):
    # Minúsculas y elimina caracteres especiales
    texto = texto.lower()
    
    # Elimina tildes
    texto = unidecode(texto)
    
    # Elimina puntuacion y numeros
    texto = re.sub(r'[^a-z\s]', '', texto)
    
    #Tokeniza
    tokens = texto.split()
    
    # Elimina stopwords
    tokens_limpios = [token for token in tokens if token not in STOPWORDS]
    
    return tokens_limpios

# 4) Cálculo de TF-IDF
def construir_modelo_tfidf(textos_tokenizados):
    print("Construyendo modelo TF-IDF...")
    
    N = len(textos_tokenizados) # Número total de documentos
    
    vocabulario = set()
    contador  = Counter()
    
    for tokens in textos_tokenizados:
        vocabulario.update(tokens)
        unique_tokens_in_doc = set(tokens)
        contador.update(unique_tokens_in_doc)
        
    vocabulario_ordenado = sorted(list(vocabulario))
    
    # Calculo de IDF
    #  IDF(t) = log( N / (1 + DF(t)) )
    idf_map = {}
    for termino in vocabulario_ordenado:
        df = contador.get(termino, 0) # DF(t)
        idf_map[termino] = math.log(N / (1 + df))

    # Calculo de TF y Matriz TF-IDF
    tfidf_matriz = []
    
    for tokens in textos_tokenizados:
        doc_vector = []
        contador_tf = Counter(tokens)
        tokens_en_doc = len(tokens)
        
        if tokens_en_doc == 0:
            doc_vector = [0.0] * len(vocabulario_ordenado)
        else:
            for termino in vocabulario_ordenado:
                tf = contador_tf.get(termino, 0) / tokens_en_doc
                tf_idf = tf * idf_map.get(termino, 0)
                doc_vector.append(tf_idf)
        
        tfidf_matriz.append(np.array(doc_vector)) # Usamos array de numpy

    print("Modelo TF-IDF construido.")
    return vocabulario_ordenado, idf_map, tfidf_matriz

# Similitud del Coseno

def similitud_coseno(vec1, vec2):
    
    #Implementa la formula de similitud del coseno usando NumPy
    producto_punto = np.dot(vec1, vec2)
    norma_vec1 = np.linalg.norm(vec1)
    norma_vec2 = np.linalg.norm(vec2)
    
    if norma_vec1 == 0 or norma_vec2 == 0:
        return 0.0 # Evita division por cero
    
    return producto_punto / (norma_vec1 * norma_vec2)

#   6 Funciones de Clasificación

def vectorize_query(query_tokens, vocabulario_ordenado, idf_map):
    """
    Convierte una query (ya tokenizada) en un vector TF-IDF.
    Usa los valores IDF ya calculados del modelo
    """
    vector_query = []
    contador_tf = Counter(query_tokens)
    e = len(query_tokens)
    
    if e == 0:
        return np.zeros(len(vocabulario_ordenado))

    for termino in vocabulario_ordenado:
        tf = contador_tf.get(termino, 0) / e
        valor_idf = idf_map.get(termino, 0.0) 
        tf_idf = tf * valor_idf
        vector_query.append(tf_idf)
        
    return np.array(vector_query)

def clasificacion_query(query_texto, model, k):
    """
    Proceso de clasificacion de una query
    """
    vocabulario, idf_map, tfidf_matriz, doc_categories = model
    
    # 1. Procesar y Vectorizar Query
    query_tokens = preprocesar_texto(query_texto)
    vector_query = vectorize_query(query_tokens, vocabulario, idf_map)

    # 2. Calcular Similitud
    similitudes = []
    for i, vector_doc_base in enumerate(tfidf_matriz):
        categoria_doc = doc_categories[i]
        sim = similitud_coseno(vector_query, vector_doc_base)
        similitudes.append((sim, categoria_doc))

    # 3. Ordenar resultados
    similitudes.sort(key=lambda x: x[0], reverse=True)
    
    # 4. Seleccionar K vecinos
    k_vecinos = similitudes[:k]
    
    # 5. Votación mayoritaria
    categorias_vecinos = [categoria for sim, categoria in k_vecinos]
    votacion = Counter(categorias_vecinos)
    
    if not votacion:
        return "Desconocida", "No hubo vecinos K."
        
    categoria_ganadora, num_votos = votacion.most_common(1)[0]
    
    # 6. Justificacion
    detalle_votos = ", ".join(f"'{cat}': {votos}" for cat, votos in votacion.items())
    
    return categoria_ganadora, detalle_votos


if __name__ == "__main__":

    # Cargar y Preprocesar
    documentos = cargar_documentos_desde_disco(RUTA_DATASET)
    
    if documentos:
        doc_categories = [cat for cat, texto in documentos]
        textos_tokenizados = [preprocesar_texto(texto) for cat, texto in documentos]
        
        # Construir Modelo
        vocabulario, idf_map, tfidf_matriz = construir_modelo_tfidf(textos_tokenizados)
        model = (vocabulario, idf_map, tfidf_matriz, doc_categories)
        
        print("-" * 60)
        
        # Textos de Consulta
        queries_prueba = [
            "A new rocket is going to the moon and mars. Space exploration is important.", # (sci.space)
            "The hockey player scored the final goal during the playoffs.",               # (rec.sport.hockey)
            "The president and the prime minister are discussing new middle east policies.", # (talk.politics.mideast)
            "This new algorithm renders 3D graphics much faster using the GPU."           # (comp.graphics)
        ]
        
        print(f"Iniciando clasificacion de {len(queries_prueba)} queries (K={K_VECINOS})...")
        
        # Probar y Mostrar Resultados
        for i, query in enumerate(queries_prueba):
            categoria_pred,detalle_votos = clasificacion_query(query, model, K_VECINOS)
            
            print(f"\n--- QUERY {i+1} ---")
            print(f"Texto: \"{query}\"")
            print(f"  -> Categoria Asignada: [{categoria_pred}]")
            print(f"  -> Justificacion (Votacion K={K_VECINOS}): {detalle_votos}") 
    
    else:
        print("Ejecucion detenida. No se pudieron cargar los documentos.")