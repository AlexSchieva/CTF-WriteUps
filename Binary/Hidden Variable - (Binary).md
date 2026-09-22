---
titolo: "Write-up: Hidden Variable - Binary"
data: 2026-09-23
categoria: Binary
tags:
  - global_var
---
## 1. Informazioni Generali
* **Piattaforma:** [olicyber.training.it]
* **Difficoltà:** [Facile] 
## 2. Analisi delle vulnerabilità
La challenge richiede di trovare una variabile nascosta. Se si analizza il file con Ghidra e si controlla la cartella **_exports_**, che contiene tutte le variabili globali che non sono state dichiarate come **_static_**, si trova una variabile chiamata **_fl4g_** 
## 3. Exploitation
Per poter leggere la variabile in maniera chiara si clicca tasto destro sulla variabile, **data** > **choose Data Type** e si imposta **unicode32**, e si legge la flag:
```
flag{unu53d_v4r5_4r3_5711_c0mp1l3d}
```