125053972 - Ticket promedio (ingreso promedio por registro) por tienda.

PASOS PARA REPRODUCIR: 
cp .env.example .env   
  python3 scripts/generar_dataset.py 125053972   
  docker compose up --build -d 

real	0m40.819s
user	0m58.539s
sys	0m2.221s

COMPARATIVA DE RENDIMINETO
El script secuencial en Python tardo 9.88 s y el job de Hadoop Streaming tardó 40.82 s (real 0m40.819s), por lo que el secuencial fue mas rapido. La salida de ambos fue identica, verificado con diff (“RESULTADOS COINCIDEN”). Esto se debe a que Hadoop se ejecuta en modo standalone, en una sola maquina y sin paralelismo real. El tiempo de CPU del job (user 58.5 s) fue mayor que su tiempo real (40.8 s), lo que indica que hubo cierto trabajo concurrente, pero no el suficiente para superar a una sola pasada secuencial que solo acumula unas decenas de tiendas en memoria. MapReduce conviene cuando los datos exceden la capacidad de una sola máquina y hay varios nodos que procesen bloques en paralelo.

A1 DOCKERFILE HADOOP: 
Compiled by ubuntu on 2023-06-18T08:22Z
Compiled on platform linux-x86_64
Compiled with protoc 3.7.1
From source with checksum 5652179ad55f76cb287d9c633bb53bbd
This command was run using /opt/hadoop/share/hadoop/common/hadoop-common-3.3.6.jar

Parte E. TEORIA 

1. Diferencia entre los modos standalone, pseudo-distribuido y totalmente distribuido de Hadoop. ¿En cuál de ellos se usa HDFS? Standalone es una sola JVM, sin demonios, y usa el sistema de archivos local. Pseudo-distribuido ejecuta los demonios (NameNode, DataNode, etc.) como procesos separados en una sola máquina y requiere SSH. Totalmente distribuido corre en un clúster de varias máquinas. HDFS se usa en pseudo-distribuido y distribuido, no en standalone.

2. ¿Por qué el dataset se monta como volumen y no se copia dentro de la imagen con COPY?, Menciona al menos dos razones.
Con COPY la imagen pesaría 400 MB más, los builds serían lentos y el dato quedaría atado a la imagen. Además el dataset depende de cada matrícula y no debe versionarse ni subirse al repo. Un volumen de solo lectura permite cambiar el dato sin reconstruir y protege el original.

3. ¿Qué ocurre con los datos de la base de datos al ejecutar docker compose down? ¿Y con docker compose down -v?
docker compose down elimina contenedores y red, pero los volúmenes nombrados persisten, así que los datos de la BD siguen. down -v también borra los volúmenes y se pierden los datos.

4. ¿Por qué MapReduce no siempre es más rápido que un script secuencial con un archivo de 400 MB? ¿A partir de qué condiciones conviene? Hay sobrecarga fija y con 400 MB en una sola maquina no hay paralelismo que compense. Conviene cuando los datos exceden la memoria o el disco de una maquina, hay varios nodos y se aprovecha la localidad de datos en HDFS.

5. Diferencia entre CMD y ENTRYPOINT, y entre COPY y ADD.
ENTRYPOINT define el ejecutable fijo y CMD el comando o argumentos por defecto, fácilmente sobreescribibles (aquí entrypoint.sh + CMD tail -f /dev/null). COPY vs. ADD: COPY solo copia archivos locales. ADD además descomprime tar locales y admite URLs, por lo que se prefiere COPY.
