# classifier.py
import os
import re
import math
from collections import Counter

class ClasificadorTextos:
    def __init__(self):
        self.categorias = []
        self.documentos = []
        self.vocabulario = set()
        self.vectores_tfidf = {}
        self.valores_idf = {}
        self.stopwords = self._obtener_stopwords()
    
    def _obtener_stopwords(self):
        """Palabras comunes que no aportan significado"""
        palabras_comunes = {
            'de', 'la', 'que', 'el', 'en', 'y', 'a', 'los', 'del', 'se', 
            'las', 'por', 'un', 'para', 'con', 'no', 'una', 'su', 'al', 
            'lo', 'como', 'más', 'pero', 'sus', 'le', 'ya', 'o', 'este', 
            'sí', 'porque', 'esta', 'entre', 'cuando', 'muy', 'sin', 'sobre', 
            'también', 'me', 'hasta', 'hay', 'donde', 'quien', 'desde', 
            'todo', 'nos', 'durante', 'todos', 'uno', 'les', 'ni', 'contra', 
            'otros', 'ese', 'eso', 'ante', 'ellos', 'e', 'esto', 'mí', 
            'antes', 'algunos', 'qué', 'unos', 'yo', 'otro', 'otras', 
            'otra', 'él', 'tanto', 'esa', 'estos', 'mucho', 'quienes', 
            'nada', 'muchos', 'cual', 'poco', 'ella', 'estar', 'estas'
        }
        return palabras_comunes
    
    def _limpiar_texto(self, texto):
        """Limpia el texto: minúsculas y quita caracteres raros"""
        texto = texto.lower()
        
        # Quitar tildes de forma simple
        texto = texto.replace('á', 'a').replace('é', 'e')
        texto = texto.replace('í', 'i').replace('ó', 'o')
        texto = texto.replace('ú', 'u')
        
        # Quitar números y símbolos, dejar solo letras
        texto = re.sub(r'[^a-z\s]', '', texto)
        
        return texto
    
    def _dividir_palabras(self, texto):
        """Separa el texto en palabras individuales"""
        return texto.split()
    
    def _quitar_palabras_comunes(self, palabras):
        """Elimina palabras que no aportan significado"""
        return [p for p in palabras if p not in self.stopwords and len(p) > 2]
    
    def preprocesar_texto(self, texto):
        """Aplica todo el procesamiento al texto"""
        texto_limpio = self._limpiar_texto(texto)
        palabras = self._dividir_palabras(texto_limpio)
        palabras_filtradas = self._quitar_palabras_comunes(palabras)
        return palabras_filtradas
    
    def cargar_datos(self, ruta_dataset):
        """Carga los documentos desde las carpetas"""
        self.categorias = []
        self.documentos = []
        
        for categoria in os.listdir(ruta_dataset):
            ruta_categoria = os.path.join(ruta_dataset, categoria)
            if os.path.isdir(ruta_categoria):
                self.categorias.append(categoria)
                
                for archivo in os.listdir(ruta_categoria):
                    if archivo.endswith('.txt'):
                        ruta_archivo = os.path.join(ruta_categoria, archivo)
                        with open(ruta_archivo, 'r', encoding='utf-8', errors='ignore') as f:
                            contenido = f.read()
                        
                        self.documentos.append({
                            'categoria': categoria,
                            'contenido': contenido,
                            'palabras': self.preprocesar_texto(contenido)
                        })
        
        print(f"Se cargaron {len(self.documentos)} documentos de {len(self.categorias)} categorías")
    
    def construir_vocabulario(self):
        """Crea la lista de todas las palabras únicas"""
        self.vocabulario = set()
        for doc in self.documentos:
            self.vocabulario.update(doc['palabras'])
        print(f"Vocabulario: {len(self.vocabulario)} palabras diferentes")
    
    def calcular_tf(self, palabras):
        """Calcula frecuencia de términos en un documento"""
        total_palabras = len(palabras)
        contador = Counter(palabras)
        tf = {palabra: cuenta / total_palabras for palabra, cuenta in contador.items()}
        return tf
    
    def calcular_idf(self):
        """Calcula IDF para todas las palabras"""
        total_docs = len(self.documentos)
        frecuencia_docs = {}
        
        # Contar en cuántos documentos aparece cada palabra
        for palabra in self.vocabulario:
            cuenta = sum(1 for doc in self.documentos if palabra in doc['palabras'])
            frecuencia_docs[palabra] = cuenta
        
        # Calcular IDF
        self.valores_idf = {}
        for palabra, df in frecuencia_docs.items():
            self.valores_idf[palabra] = math.log(total_docs / (1 + df))
    
    def calcular_vectores_tfidf(self):
        """Calcula vectores TF-IDF para todos los documentos"""
        self.vectores_tfidf = {}
        
        for i, doc in enumerate(self.documentos):
            tf = self.calcular_tf(doc['palabras'])
            vector_tfidf = {}
            
            for palabra in self.vocabulario:
                valor_tf = tf.get(palabra, 0)
                valor_idf = self.valores_idf.get(palabra, 0)
                vector_tfidf[palabra] = valor_tf * valor_idf
            
            self.vectores_tfidf[i] = {
                'vector': vector_tfidf,
                'categoria': doc['categoria']
            }
        
        print("Vectores TF-IDF calculados")
    
    def similitud_coseno(self, vec1, vec2):
        """Calcula qué tan parecidos son dos textos"""
        # Producto punto
        producto = 0
        for palabra in self.vocabulario:
            producto += vec1.get(palabra, 0) * vec2.get(palabra, 0)
        
        # Normas de los vectores
        norma1 = math.sqrt(sum(v * v for v in vec1.values()))
        norma2 = math.sqrt(sum(v * v for v in vec2.values()))
        
        # Evitar división por cero
        if norma1 == 0 or norma2 == 0:
            return 0
        
        return producto / (norma1 * norma2)
    
    def clasificar_consulta(self, texto_consulta, k=5):
        """Clasifica un texto nuevo usando los k más cercanos"""
        # Procesar la consulta
        palabras_consulta = self.preprocesar_texto(texto_consulta)
        tf_consulta = self.calcular_tf(palabras_consulta)
        
        # Crear vector TF-IDF para la consulta
        vector_consulta = {}
        for palabra in self.vocabulario:
            tf_valor = tf_consulta.get(palabra, 0)
            idf_valor = self.valores_idf.get(palabra, 0)
            vector_consulta[palabra] = tf_valor * idf_valor
        
        # Calcular similitudes con todos los documentos
        similitudes = []
        for doc_id, doc_data in self.vectores_tfidf.items():
            similitud = self.similitud_coseno(vector_consulta, doc_data['vector'])
            similitudes.append({
                'doc_id': doc_id,
                'similitud': similitud,
                'categoria': doc_data['categoria']
            })
        
        # Ordenar de mayor a menor similitud
        similitudes.sort(key=lambda x: x['similitud'], reverse=True)
        
        # Tomar los k más similares
        vecinos_cercanos = similitudes[:k]
        
        # Contar votos por categoría
        votos_categoria = {}
        for vecino in vecinos_cercanos:
            cat = vecino['categoria']
            votos_categoria[cat] = votos_categoria.get(cat, 0) + 1
        
        # La categoría con más votos gana
        categoria_ganadora = max(votos_categoria.items(), key=lambda x: x[1])[0]
        
        return {
            'categoria_predicha': categoria_ganadora,
            'similitudes': similitudes[:5],
            'vecinos': vecinos_cercanos,
            'votos': votos_categoria
        }
    
    def entrenar(self, ruta_dataset):
        """Entrena el clasificador con los datos"""
        print("Cargando datos...")
        self.cargar_datos(ruta_dataset)
        
        print("Construyendo vocabulario...")
        self.construir_vocabulario()
        
        print("Calculando IDF...")
        self.calcular_idf()
        
        print("Calculando vectores TF-IDF...")
        self.calcular_vectores_tfidf()
        
        print("Listo para clasificar!")