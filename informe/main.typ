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
Simulación comparativa de TLS 1.2, TLS 1.3 y etc.

\
\
\


\
\
],
  author:"Lya Díaz Roa\nhugodiazroa: https://github.com/hugodiazroa", 
  date: datetime(year: 2024, month: 12, day: 09),
  abstract: [

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
TLS es la base de la comunicación segura en Internet, ya que ofrece cifrado robusto, autenticación y eficiencia. Este proyecto desarrolla un sistema para simular su funcionamiento, centrándose en el proceso de handshake. Este sistema informático compara TLS 1.3 con TLS 1.2, mostrando las mejoras y comparándolas con una versión mala de TLS (TLS etc.) hecha por mí.

\
== TLS etc.

"TLS etc." es una version de TLS hecha por mi e implementada usando firmas y encripcion de Pretty Good Privacy (PGP). Esto es poco practico por muchos motivos, pero el mas obvio es el de lentitud y encripciones mucho mas grandes que las de TLS 1.2 y TLS 1.3.

\
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
== Conclusión

TLS 1.3 ha sido ampliamente referenciado en la investigación por su sólida seguridad, rendimiento mejorado y avances respecto a versiones anteriores. Está ampliamente implementado en navegadores, servidores y servicios en la nube, lo que pone de relieve su impacto práctico. El protocolo sigue siendo muy relevante, abordando los retos de seguridad modernos e inspirando mejoras continuas, como la criptografía resistente a la cuántica y los mecanismos 0-RTT mejorados. Estos avances refuerzan el papel fundamental de TLS 1.3 en la comunicación segura.