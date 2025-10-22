# main.py
from classifier import ClasificadorTextos
from queries import consultas_prueba
import os

def main():
    # Verificar que existe el dataset
    if not os.path.exists('dataset'):
        print("Error: No hay dataset")
        print("Ejecuta: python crear_dataset.py")
        return
    
    # Crear y entrenar el clasificador
    clasificador = ClasificadorTextos()
    clasificador.entrenar('dataset')
    
    print("\n" + "="*50)
    print("PRUEBA DEL CLASIFICADOR")
    print("="*50)
    
    # Probar con las consultas
    correctas = 0
    total = len(consultas_prueba)
    
    for i, consulta in enumerate(consultas_prueba, 1):
        print(f"\n--- Prueba {i} ---")
        print(f"Texto: {consulta['texto']}")
        print(f"Esperada: {consulta['categoria_esperada']}")
        
        resultado = clasificador.clasificar_consulta(consulta['texto'])
        
        print(f"Obtenida: {resultado['categoria_predicha']}")
        
        if resultado['categoria_predicha'] == consulta['categoria_esperada']:
            correctas += 1
            print("✅ Correcto")
        else:
            print("❌ Incorrecto")
        
        print("Votos:", resultado['votos'])
        
        print("Top 3 similares:")
        for j, sim in enumerate(resultado['similitudes'][:3], 1):
            print(f"  {j}. {sim['similitud']:.3f} - {sim['categoria']}")
    
    # Resultado final
    print("\n" + "="*50)
    print("RESULTADO FINAL")
    print("="*50)
    precision = (correctas / total) * 100
    print(f"Precisión: {correctas}/{total} ({precision:.1f}%)")

if __name__ == "__main__":
    main()