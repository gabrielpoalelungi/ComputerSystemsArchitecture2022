# Marketplace_ASC
331CC - Poalelungi Gabriel
Aprilie 2022

Tema 1 - Marketplace

Organizare:

    1) Pentru implementarea metodelor din toate cele 3 clase, m-am folosit de urmatoarele variabile din clasa Marketplace:
        - 'products': reprezinta o lista de liste de tipul [id_producer, produs, lock_produs, disponibilitate_produs]
            - 'id_producer' este generat de metoda register_producer() din clasa Marketplace
            - 'produs' este un obiect de tip Coffee sau Tea
            - 'lock_produs' este Lock()-ul asociat produsului astfel incat disponibilitatea sa fie schimbata thread-safe
            - 'disponiblitate_produs' este un boolean care arata daca produsul e disponibil consumatorilor (True) sau nu (False)
        - 'producer_ids': reprezinta un dictionar care stocheaza, pentru fiecare producer, cate produse a publicat acesta.
        - 'products_lock': un Lock() folosit pentru a izola operatiile de adaugare sau scoatere din lista 'products'
        - 'carts_id': reprezinta un dictionar care stocheaza, pentru fiecare cart_id, liste de produse adaugate
        - 'carts_lock': un Lock() folosit pentru a izola operatiile de adaugare sau scoatere din lista de produse ale unui cos

    2) Explicatii pentru functionare metodelor/functiilor se afla in comentariile din cod.

    3) Consider ca tema este utila, deoarece am consolidat mai bine functionarea paralelismului. De asemenea, am invatat sa scriu
        cod mai curat si mai eficient datorita sintaxei si coding style-ului Python.

    4) Consider ca este o abordare eficienta, deoarece nu am instructiuni repetitive imbricate prea multe, desi nu cunosc complexitatile
        operatiilor cu liste si dictionare. Am incercat sa ma folosesc de metodele Python cat mai mult.

Implementare:

    1) Intregul enunt al temei este implementat + Unittest-urile. Nu am implementat logging-ul.
    
    2) Dificultatile intampinate au fost deadlock-urile sau race-condition-urile + intelegerea
        anumitor exceptii/erori Python, precum "Coffee object is not subscriptable".

    3) Lucruri interesante
        - Cat de usor este sa scrii cod Python (inca sunt semi-socat).
        - Lucrul usor si curat cu structurile de date de genul liste, dictionare.
        - For each-urile usor de folosit.

Resurse utilizate:

    - laboratoarele de Python de la ASC.
    - W3School pentru lucrul cu liste, dictionare etc.
    - StackOverflow pentru intelegerea diferitelor tipuri de erori/exceptii.

Git:
    https://github.com/gabrielpoalelungi/Marketplace_ASC

    - Acest repo va fi facut public pe 19 aprilie 2022.
    - Voi incerca sa ii ofer acces lui Edi Staniloiu intre timp.
