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
= Historia y evolución de TLS

= Introducción

Transport Layer Security (TLS) is the cornerstone of secure communication in the modern digital age, ensuring data confidentiality, integrity, and authentication across diverse applications like web browsing, email, and VoIP. Over the years, TLS has undergone significant revisions to adapt to evolving security threats and performance demands. This document explores TLS's evolution, with a focus on TLS 1.3, its operation, key improvements, and a comparative analysis with earlier versions. We will also evaluate the code implementation simulating TLS 1.3, followed by insights into its broader importance and potential advancements.

---

== Understanding TLS and the Evolution to TLS 1.3  

=== TLS 1.1 and Its Features  

TLS 1.1, introduced in 2006, improved upon its predecessor TLS 1.0 by mitigating vulnerabilities such as the CBC (Cipher Block Chaining) padding oracle attack. Key features included:  
- Initialization Vector (IV) Security: Implemented explicit IVs to enhance CBC mode encryption by ensuring randomness for each message.  
- Backward Compatibility: Supported legacy systems but did not significantly advance key exchange or handshake mechanisms.  

Despite these improvements, TLS 1.1 quickly became obsolete due to limited enhancements in both security and performance.  

=== Advancements in TLS 1.2  

TLS 1.2, released in 2008, addressed the weaknesses of earlier versions and introduced flexibility in cryptographic operations. Key innovations included:  
1. Hashing Algorithm Flexibility: Replaced MD5 and SHA-1 with SHA-256 as default, reducing vulnerability to collisions.  
2. Authenticated Encryption: Introduced Galois/Counter Mode (GCM), providing both encryption and integrity in a single operation.  
3. Elliptic Curve Cryptography (ECC): Supported ECC for more efficient and secure key exchanges compared to RSA.  
4. Customizable Cipher Suites: Allowed negotiation of cryptographic algorithms during the handshake, increasing adaptability.  

While TLS 1.2 became the standard for over a decade, its reliance on RSA key exchanges and complex handshake mechanisms left room for optimization and modernization.  

=== TLS 1.3: A Modern Solution  

Released in 2018, TLS 1.3 redefined the protocol, prioritizing both security and performance. It simplified the handshake process, eliminated legacy algorithms, and reduced latency. Major features of TLS 1.3 include:  

1. Simplified Handshake Process:  
   - Reduced latency by requiring a single round-trip for handshake completion (down from two in TLS 1.2).  
   - Introduced "0-RTT" (Zero Round-Trip Time) resumption, enabling near-instant secure connections for repeat sessions.  
   
2. Forward Secrecy by Default:  
   - Adopted ephemeral Diffie-Hellman (DHE) for key exchanges, ensuring that session keys cannot be compromised even if long-term private keys are leaked.  
   
3. Streamlined Cipher Suites:  
   - Removed weak and obsolete algorithms like RSA key exchange, MD5, and static Diffie-Hellman.  
   - Standardized AES-GCM, AES-CCM, and ChaCha20-Poly1305 for encryption.  
   
4. Improved Privacy:  
   - Encrypted more handshake data, including the server certificate, to reduce information visible to attackers.  


= Comparison of TLS Versions  

#table(
  columns: 4,
  [], [TLS 1.1], [TLS 1.2], [TLS 1.3],

  [Key Exchange], [RSA], [RSA, DHE, ECDHE], [ECDHE only],
  [Hashing Algorithm], [MD5, SHA-1], [SHA-256], [SHA-256],
  [Handshake Latency], [2 round-trips], [2 round-trips], [1 round-trip (0-RTT optional)],
  [Cipher Suites], [Static, CBC-based algorithms], [Configurable, including GCM], [Streamlined, AEAD only],
  [Forward Secrecy], [Optional], [Optional], [Mandatory],
  [Obsolete Features Removed], [No], [No], [Yes],
)


== Reviewing the TLS 1.3 Code Simulation  

The provided Python code successfully simulates key aspects of TLS 1.3, including:  
1. Key Agreement: The code uses ephemeral Diffie-Hellman (ECDHE) for secure key exchange.  
2. Handshake Simulation: It illustrates the exchange of random values, public keys, and derivation of session keys using HKDF.  
3. Encryption and Decryption: AES-GCM encryption ensures data confidentiality, while integrity is preserved through authenticated encryption.  
4. Certificate Validation: A simulated Certificate Authority (CA) issues signed certificates for verifying server authenticity.  

=== Strengths  
- Clarity: The code provides explicit logs for every step, aiding analysis of the handshake and encryption process.  
- Modern Practices: It leverages cryptographic libraries for secure implementation of TLS features.  

=== Areas for Improvement  
- Certificate Details: Expand on the CA's functionality to include validation of certificate chains and expiration checks.  
- Error Handling: Add robust exception handling to manage edge cases like invalid keys or failed encryption operations.  
- Performance Testing: Include metrics to measure the simulation's efficiency compared to TLS 1.2.  

---

== Conclusion  

The evolution of TLS, culminating in TLS 1.3, exemplifies the critical role of secure communication protocols in a digitally interconnected world. As the backbone of internet security, TLS safeguards the privacy and integrity of countless daily interactions, from online banking to remote work and cloud-based services. The advancements in TLS 1.3, particularly its streamlined handshake, mandatory forward secrecy, and elimination of legacy vulnerabilities, demonstrate how cryptographic innovation can address both longstanding and emerging security challenges.  

The importance of studying TLS lies not only in understanding how it protects data but also in its broader implications for trust in digital systems. Secure protocols like TLS enable the proliferation of technologies such as IoT, 5G networks, and decentralized applications, ensuring they operate safely and efficiently. TLS 1.3's emphasis on performance and security sets a new standard for cryptographic protocols, paving the way for advancements in areas like quantum-resistant encryption and zero-trust architectures.  

Beyond technical applications, TLS also highlights the necessity of ongoing collaboration between academia, industry, and standards bodies to adapt to an ever-changing threat landscape. Its impact extends far beyond web browsers, underscoring the significance of robust security mechanisms in fostering innovation and maintaining the stability of our increasingly digital society.
