#import "@preview/ilm:0.1.2": *


#set table(
  stroke: none,
  gutter: 0.2em,
  fill: (x, y) =>
    if x == 0 or y == 0 { gray },
  inset: (right: 1.5em),
)


#show table: set par(justify: false)
#show: ilm.with(
  title: [ #figure(
    grid(
        columns: (auto, auto, auto),
        rows:    (auto, auto, auto),
        [ #image("fcfm_dcc_png.png", width: 80%) ],
        [ #image("logo uchile.png", width: 60%)],
        [ #image("dcc_2019.png", width: 60%)],
        
    )
)

#show table.cell: it => {
  if it.x == 0 or it.y == 0 {
    set text(white)
    strong(it)
  } else if it.body == [] {
    // Replace empty cells with 'N/A'
    pad(..it.inset)[_N/A_]
  } else {
    it
  }
}



\
\

  Simulador de TLS:
Simulación comparativa de TLS 1.2 y TLS 1.3

\
\
\


\
\
\

],
  author:"Lya Díaz Roa\nhugodiazroa: https://github.com/hugodiazroa", 
  date: datetime(year: 2025, month: 02, day: 28),
  abstract: [
Este documento presenta un simulador de TLS diseñado para comparar las versiones 1.2 y 1.3 del protocolo, así como una versión experimental desarrollada por el autor. Se centra en el proceso de handshake y explora las mejoras y diferencias entre estas versiones. La simulación proporciona una comprensión clara de las ventajas de TLS 1.3 en términos de seguridad y rendimiento, y sirve como una herramienta educativa para aquellos interesados en la evolución de los protocolos de seguridad en la comunicación digital.
    ],

  chapter-pagebreak: false,
  figure-index: false,
  table-index: false,
  listing-index: false,
)

\
= Introducción

\
== Simulación de TLS
TLS es la base de la comunicación segura en Internet, ya que ofrece cifrado robusto, autenticación y eficiencia. Este proyecto desarrolla un sistema para simular su funcionamiento, centrándose en el proceso de handshake. Este sistema informático compara TLS 1.3 con TLS 1.2.


\
= Historia y evolución de TLS

La seguridad de la capa de transporte (TLS, por Transport Layer Security) es la piedra angular de la comunicación segura en la era digital moderna, ya que garantiza la confidencialidad, integridad y autenticación de los datos en diversas aplicaciones como HTTPS, Tor, correos electrónicos y VoIP. A lo largo de los años, TLS se ha sometido a importantes revisiones para adaptarse a la evolución de las amenazas a la seguridad que trajo el desarrollo de la criptografía. El presente documento explora la evolución de TLS, centrándose en la comparativa entre TLS 1.2, TLS 1.3 y una versión de TLS improvisada por el autor. Esto se logrará mediante la implementación de código que simula estas versiones de TLS, en específico el handshake (apretón de manos).

\
== Comprendiendo TLS y su evolución a TLS 1.3

=== TLS 1.1 y sus características

Introducido en 2006, TLS 1.1 mejoró TLS 1.0 al abordar vulnerabilidades como el ataque de oráculo de relleno CBC (Cipher Block Chaining), mejorando notablemente el cifrado en modo CBC con vectores de inicialización explícitos para garantizar la aleatoriedad de los mensajes, al tiempo que mantenía la compatibilidad con sistemas heredados. Sin embargo, ofrecía avances mínimos en los mecanismos de intercambio de claves y handshake, lo que provocó su rápida obsolescencia debido a las limitadas mejoras tanto en seguridad como en rendimiento.

=== Avances en TLS 1.2

Lanzada en 2008, TLS 1.2 solucionó vulnerabilidades presentes en versiones anteriores e introdujo mejoras significativas en las operaciones criptográficas. Entre sus principales innovaciones se encuentra la flexibilidad para elegir algoritmos hash seguros, sustituyendo los anticuados MD5 y SHA-1 por SHA-256 por defecto, reduciendo así la susceptibilidad a las colisiones. La introducción del Modo Galois/Contador (GCM) mejoró la seguridad al combinar el cifrado y la verificación de la integridad en una sola operación. Además, TLS 1.2 incorporó soporte para Criptografía de Curva Elíptica (ECC), ofreciendo mecanismos de intercambio de claves más eficientes y seguros en comparación con el tradicional RSA. Otra mejora notable fue la capacidad de negociar suites de cifrado personalizables durante el proceso de apreton de manos, lo que proporciona una mayor adaptabilidad a los distintos requisitos de seguridad.

A pesar de sus avances, TLS 1.2 no estaba exento de limitaciones. Su dependencia de los intercambios de claves RSA y la complejidad de sus mecanismos de negociación pusieron de manifiesto la necesidad de optimización y modernización. No obstante, TLS 1.2 marcó la pauta de las comunicaciones seguras durante más de una década, salvando las distancias entre las vulnerabilidades de protocolos anteriores y los sólidos avances introducidos en iteraciones posteriores.


=== TLS 1.3: una solución moderna

Lanzado en 2018, TLS 1.3 aportó avances significativos a la comunicación segura en Internet al centrarse tanto en la seguridad como en el rendimiento. El protocolo simplificó el proceso de enlace, eliminó algoritmos obsoletos y redujo la latencia de la conexión. Una de sus mejoras más notables es la simplificación del protocolo de enlace, que ahora requiere un único viaje de ida y vuelta para establecer una conexión segura, frente a los dos de TLS 1.2. Además, introduce la reanudación «0-RTT», que permite conexiones seguras casi instantáneas para sesiones repetidas.

TLS 1.3 también da prioridad a las medidas de seguridad sólidas. El secreto de transmisión se aplica por defecto mediante el uso de intercambios efímeros de claves Diffie-Hellman, lo que garantiza que las claves de sesión permanezcan seguras incluso si las claves privadas a largo plazo se ven comprometidas. El protocolo ha simplificado las suites de cifrado, eliminando algoritmos débiles como el intercambio de claves RSA y MD5, y estandarizando métodos de cifrado modernos como AES-GCM, AES-CCM y ChaCha20-Poly1305. La privacidad mejora aún más al cifrar más datos del protocolo de enlace, incluido el certificado del servidor, lo que reduce la información disponible para posibles atacantes.
#pagebreak()
= Funcionamiento interno del apreton de manos de TLS

TLS tiene un proceso de handshake que se compone de varias etapas. En TLS 1.2, el handshake consta de dos viajes de ida y vuelta, mientras que en TLS 1.3 se reduce a un solo viaje de ida y vuelta. A continuación, se detallan las etapas del handshake en ambas versiones:
== TLS 1.2

TLS 1.2 consta de las siguientes etapas en el proceso de apreton de manos:
1. Cliente envía un mensaje "ClientHello" al servidor con:
    - Versiónes de TLS soportadas
    - Número aleatorio con bits de tiempo y aleatorios
    - Identificador de sesión
    - Suites de cifrado soportadas
    - Extensiones

2. Servidor responde con un mensaje "ServerHello" que contiene:
    - Versión de TLS seleccionada
    - Número aleatorio con bits de tiempo y aleatorios
    - Identificador de sesión
    - Suite de cifrado seleccionada
    - Certificado del servidor
    - Parámetros de intercambio de claves

3.



== TLS 1.3

1. Cliente envía un mensaje "ClientHello" al servidor con:
    - Versión de TLS soportada
    - Número aleatorio
    - Identificador de sesión
    - Suites de cifrado soportadas
    - Extensiones

2. Servidor responde con un mensaje "ServerHello" que contiene:
    - Versión de TLS seleccionada
    - Número aleatorio
    - Identificador de sesión
    - Suite de cifrado seleccionada
    - Extensiones


#pagebreak()
= El simulador

Nuestro simulador de TLS se basa en un modelo simplificado del proceso de handshake de TLS 1.2 y TLS 1.3.
La diferencia radica en que se han eliminado pasos para simplificar el proceso y centrarse en las diferencias clave entre las versiones, asi como en los pricipios criptograficos que hacen funcionar a TLS 1.3.
En particular, el simulador muestra un acuerdo de llave usando el algoritmo de intercambio de llaves Diffie-Hellman, que es usado por TLS 1.3 para garantizar la seguridad de las llaves de sesion.
En vez de mandar un numero aleatorio en el clientHello, se manda una exponenciacion modular de un numero aleatorio con un generador de numeros primos, que es el secreto compartido entre el cliente y el servidor.
\
Otra diferencia que se puede apreciar es el cambio del certificado x509 por el uso de PGP. Esto se debe a que no se logro implementar el uso de certificados x509 en el simulador, por lo que se opto por usar algo similar.
Este protocolo se usa en la parte de la simulacion de TLS 1.2, para acordan una llave simetrica entre el cliente y el servidor usando RSA.
\
\
El simulador usa una GUI escrita en Python con la libreria Tkinter, que permite al usuario ver las ejecuciones de TLS 1.2 y TLS 1.3 de forma mas amigable.
Dentro de esta interfaz hay tres botones, uno para ejecutar TLS 1.2, otro para TLS 1.3 y otro para limpiar la pantalla.
Una vez que se ejecuta uno de los protocolos, se muestra en la pantalla la informacion de los mensajes enviados y recibidos, asi como el acuerdo de llave y el mensaje de confirmacion de la llave.
Los mensajes estan coloreados para diferenciar entre explicaciones, notas, los mensajes enviados por el cliente y los mensajes enviados por el servidor.

== Demo

A continuacion se muestra una demostracion del simulador de TLS, donde se ejecuta TLS 1.2 y TLS 1.3, mostrando los mensajes enviados y recibidos, el acuerdo de llave y el mensaje de confirmacion de la llave.



#pagebreak()
= Comparación de versiones de TLS

#table(
  columns: 4,
  [], [TLS 1.1], [TLS 1.2], [TLS 1.3],

  [Intercambio de claves], [RSA], [RSA, DHE, ECDHE], [Sólo ECDHE],
  [Algoritmo hash], [MD5, SHA-1], [SHA-256], [SHA-256],
  [Latencia de Handshake], [2 viajes de ida y vuelta], [2 viajes de ida y vuelta], [1 viaje de ida y vuelta (0-RTT opcional)],
  [Suites de cifrado], [Algoritmos estáticos basados en CBC], [Configurable, incluido GCM], [Optimizado, sólo AEAD],
  [Secreto hacia adelante], [Opcional], [Opcional], [Obligatorio],
  [Características obsoletas eliminadas], [No], [No], [Sí],

)

#pagebreak()
= Conclusión
