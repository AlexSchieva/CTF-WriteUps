---
titolo: "Write-up: Sn4ck sh3nan1gans - SQLi"
data: 2026-09-22
categoria: Web
tags:
  - sqli
---
## 1. Informazioni Generali
* **Piattaforma:** [olicyber.training.it]
* **Difficoltà:** [Media] 
* **Risorsa:** [http://sn4ck-sh3nan1gans.challs.olicyber.it](http://sn4ck-sh3nan1gans.challs.olicyber.it)

## 2. Analisi delle vulnerabilità
La pagina mostra una pagina di login e una pagina di registrazione. Registrandosi e facendo il login si apre una pagina con la scritta **Welcome _nome utente_**. Tentando di fare delle SQLi sui form di login/registrazione non succede nulla. A questo punto se si va ad ispezionare la richiesta **POST** che viene mandata tramite il **login** si vede che contiene un **cookie** chiamato _login_, la cui conversione da base64 è un oggetto JSON del tipo
```json
{"ID":113}
```
Andando a modificare il cookie nella richiesta, impostando come ID un numero diverso, e inviandola si nota che la pagina mostra come nome utente quello di un'altra persona, aggirando di fatto il login con username e password. Si pressupone quindi che venga fatta una query SQL in cui si prende l'ID e si restituisce il nome dell'utente a cui è associato. 
A questo punto, verrebbe da provare tramite script a inviare richieste modificando il valore del cookie e vedere se viene mostrato qualcosa di interessante, ma nulla. Quindi si tenta con una SQLi e si nota che effettivamente funziona.
## 3. Exploitation
Come detto prima, si può iniettare del codice SQL all'interno del cookie per sfruttare una SQLi. Di seguito il cookie con  l'iniezione da applicare alla chiamata POST a **_/home.php_**:
```json
{"ID": "0 union select table_name from information_schema.tables WHERE table_schema = DATABASE()"}
```
Il risultato che si ottiene nella pagina web della risposta è il seguente: 
```html
<h1>Welcome here_is_the_flag!</h1>
```
Abbiamo trovato che esiste una tabella chiamata così, non ci resta che iniettare una query che mostri il suo contenuto:
```json
{"ID": "0 union select * from here_is_the_flag"}
```
Inviando questo cookie il risultato è la flag: **_flag{W4sH_y0ur_HaNd5_b3f0Re_e4tin6_c0oki3s!}_**