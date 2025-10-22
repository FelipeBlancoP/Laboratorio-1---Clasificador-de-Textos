# crear_dataset.py
import os
import shutil

# Borrar dataset anterior si existe
carpeta_dataset = "dataset"
if os.path.exists(carpeta_dataset):
    shutil.rmtree(carpeta_dataset)
    print("Dataset anterior borrado")

# Datos de ejemplo MEJORADOS - más específicos por categoría
datos = {
    "tecnologia": [
        "computadora portatil laptop procesador intel windows linux programacion python java javascript html css desarrollo web aplicacion movil android ios smartphone tablet iphone samsung red wifi bluetooth usb monitor pantalla teclado mouse software hardware codigo algoritmo",
        "videojuego consola playstation xbox nintendo switch pc gaming steam graficos 4k fps resolucion textura motor unreal unity jugabilidad online multiplayer servidor latencia descarga actualizacion dlc expansion mod comunidad streamer esports torneo",
        "internet navegador chrome firefox website sitio web dominio hosting servidor ip protocolo http https seguridad firewall antivirus malware hacker password contraseña cookie cache red social facebook instagram mensajeria whatsapp email correo",
        "redes telecomunicaciones 5g fibra optica modem router ethernet lan wan vpn velocidad descarga subida latencia videollamada zoom teams streaming netflix youtube spotify podcast television smart tv iot internet cosas sensor drone robot",
        "programacion codigo fuente compilador ide visual studio git github version control repository branch commit push pull bug error exception loop function class object variable array list algorithm sort search memory",
        "base datos sql mysql postgresql query select insert update delete join index transaction table column row primary key foreign key relationship backup replication cluster performance"
    ],
    "deportes": [
        "futbol soccer balon pie campo cesped estadio cancha porteria arco gol penalty falta tarjeta amarilla roja arbitro fuera juego corner saque banda centro tiro libre defensa mediocampo delantero portero entrenador tactica formacion",
        "baloncesto basketball canasta aro tablero balon dribble pase tiro triple dos puntos libre falta rebote bloqueo tapon robo transicion ataque rapido contraataque posicion base escolta alero pivot poste penetracion pantalla mate dunk",
        "tenis raqueta pelota cancha cesped arcilla red saque servicio reves drive derecha volea smash dejada globo passing shot winner ace doble falta break punto game set match tiebreak ranking atp wta",
        "natacion piscina carril estilo libre crol espalda mariposa braza pecho viraje voltereta salida nado sincronizado saltos trampolin plataforma clavados waterpolo balon porteria gafas traje baño aletas buceo",
        "ciclismo bicicleta ruta montaña carrera tour francia giro italia contrarreloj equipo peloton escapada sprinter escalador gregario lider maillot amarillo meta montaña puerto ascenso descenso cambio marchas plato pinon",
        "beisbol baseball bate pelota guante catcher pitcher lanzador receptor base home plato jonron homerun carrera out strike bola foul hit sencillo doble triple cuadrangular inning entrada manager coach shortstop jardinero"
    ],
    "ciencia": [
        "fisica cuantica mecanica ondulatoria particula electron proton neutron atomo nucleo orbital energia quanta superposicion entrelazamiento funcion onda probabilidad incertidumbre computacion cuantica qubit fotones experimento doble rendija",
        "biologia molecular adn arn genoma gen codigo genetico secuenciacion nucleotido base replicacion transcripcion traduccion proteina aminoacido codon ribosoma mrna cromosoma mutacion delecion insercion gen supresor tumoral cancer",
        "astronomia telescopio hubble webb espacial observatorio galaxia andromeda via lactea estrella sol planeta marte jupiter saturno nebulosa agujero negro supernova quasar pulsar cosmologia big bang expansion universo materia oscura",
        "quimica organica compuesto carbono hidrogeno oxigeno nitrogeno enlace covalente molecular formula estructural isomería quiralidad centro quiral reaccion sustitucion adicion eliminacion oxidacion reduccion catalizador enzima ph acidez",
        "geologia roca ignea sedimentaria metamorfica magma lava volcan erupcion terremoto sismo falla tectonica placa litosfera manto nucleo corteza mineral cuarzo feldespato erosion meteorizacion sedimentacion fosil paleontologia",
        "neurologia cerebro neuronas sinapsis neurotransmisores dopamina serotonina sistema nervioso central periferico medula espinal nervio potencial accion despolarizacion plasticidad sinaptica aprendizaje memoria hipocampo corteza amigdala"
    ],
    "politica": [
        "gobierno estado nacion pais territorio soberania constitucion ley legislacion ejecutivo presidente primer ministro gabinete ministerio funcionario publico administracion servicio civil impuesto tributo presupuesto gasto publico congreso diputados senadores",
        "elecciones votantes urnas sufragio voto escrutinio recuento mesa electoral junta electoral registro censo padron electoral campanha propaganda comicios primarias generales referendum plebiscito candidato partido politico coalicion",
        "derecho ley justicia tribunal corte suprema constitucional apelacion juez magistrado fiscal abogado defensor demanda querella denuncia acusacion sentencia absolucion recurso prision carcel detencion arresto delito crimen",
        "economia mercado libre competencia monopolio oferta demanda precio costo beneficio utilidad inversion capital trabajo empleo desempleo salario ingreso renta impuesto iva exportacion importacion balanza comercial",
        "politica social bienestar seguridad social pension jubilacion retiro discapacidad enfermedad subsidio ayuda vivienda publica educacion publica salud publica hospital medicamento transporte publico medio ambiente",
        "relaciones internacionales diplomacia politica exterior cancilleria embajador embajata consul consulado mision diplomatica organizacion internacional onu unesco unicef tratado libre comercio integracion cooperacion desarrollo"
    ]
}

# Crear carpetas y archivos
os.makedirs(carpeta_dataset, exist_ok=True)

total_docs = 0
for categoria, textos in datos.items():
    carpeta_categoria = os.path.join(carpeta_dataset, categoria)
    os.makedirs(carpeta_categoria, exist_ok=True)
    
    for i, texto in enumerate(textos):
        nombre_archivo = os.path.join(carpeta_categoria, f"doc_{i}.txt")
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            f.write(texto)
        total_docs += 1

print(f"Dataset creado: {total_docs} documentos")
for categoria in datos.keys():
    ruta = os.path.join(carpeta_dataset, categoria)
    archivos = len([f for f in os.listdir(ruta) if f.endswith('.txt')])
    print(f" - {categoria}: {archivos} docs")