---
titolo: NFT gallery
data: 2026-10-05
categoria: Web
tags:
  - type_confusion
  - docker
---
## 1. Informazioni Generali
* **Piattaforma:** [olicyber.training.it]
* **Sezione:** [Selezione territoriale - Demo]
* **Difficoltà:** [Media] 
* **Risorsa:** [http://nft.challs.olicyber.it](http://nft.challs.olicyber.it)

## 2. Analisi delle vulnerabilità
La sfida ci mostra un sito con 3 pulsanti che indirizzano ciascuna ad una pagina con un immagine diversa. Aprendo `Dockerfile` all'interno della cartella NTF-gallery (fornita dalla sfida), troviamo queste due righe:
```dockerfile
ARG FLAG
RUN echo ${FLAG} > /flag 
```
Questo significa che la **flag** viene salvata nella radice all'interno di `/flag`. Basta quindi trovare un modo per navigare nel _file system_ e leggerla. 
A tal proposito, nel file `index.js` troviamo queste righe di codice:
```js
app.get('/nft', async (req, res) => {
    const filename = req.query.id

    for (const char of filename) {
        if (char === '.') {
            return res.send('nope')
        }
    }

    const p = path.join(__dirname, 'nft/' + filename)

    try {
        const data = await fs.readFile(p)
        res.render('nft', { base64img: data.toString('base64') })
    } catch (e) {
        res.send('Not found', 404)
    }

})
```
Vediamo che il codice blocca il tentativo di risalire le cartelle tramite il rilevamento del carattere `.`, ma si può sfruttare il **type confusion** per evitare il filtro. 
Per capire com'è la struttura del **file system** del server è possibile utilizzare impostare un **docker** con la build del _Dockerfile_ del server, andando ad attivare gli errori togliendo il costrutto **catch** dal file _index.js_, e per ultimo attivando il log dal docker tramite il comando `docker logs -f nft-gallery-webapp-1`, in modo che quando si va a testare la navigazione con `../` si sappia di quanto si deve tornare indietro per raggiungere la **root**.
## 3. Exploitation
Si fa una chiamata alla pagina `http://nft.challs.olicyber.it/nft?id[]=../flag`, in modo da passare un'array come _id_. In questo modo invece che leggere carattere per carattere, il ciclo for della funzione sopra leggerà la stringa `../../flag` come unico elemento, che non è uguale a `.`, quindi salterà il filtro e verrà restituita una pagina con un'immagine non caricata. Basterà analizzare il contenuto della pagina per vedere il tag _img_ contenente la stringa `ZmxhZ3tOMG5fZlVuZzFibDNfcDR0aH0=`, che se tradotta da **Base64** sarà la flag: 
```
flag{N0n_fUng1bl3_p4th}
```
