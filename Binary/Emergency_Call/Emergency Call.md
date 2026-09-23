---
titolo: Emergency Call
data: 2026-09-27
categoria: Binary
tags:
  - rop
---
## 1. Informazioni Generali
* **Piattaforma:** [olicyber.training.it]
* **Sezione:** [Software Security]
* **Difficoltà:** [Difficile]
* **Sfida:** ``nc emergency.challs.olicyber.it 10306``
## 2. Analisi delle vulnerabilità
Il programma chiede di inserire un numero di emergenza da chiamare e dopo di che richiede come altro input l'emergenza. Se si analizza il file scaricato con il comando `file emergency-call` si nota che è **linkato staticamente** (quindi contiene il codice delle librerie esterne di cui ha bisogno per funzionare) ed è **stripped** (tutti i **simboli di debug** sono stati rimossi, ovvero tutti i nomi in chiaro delle funzioni e delle variabili assegnati dal programmatore). Di conseguenza l'analisi con **Ghidra** dovrebbe essere più difficoltosa. Analizziamo il **main** con il decompilatore:
```C
undefined8 main(void)
{
  undefined local_28 [32];
  
  FUN_0040101d(1,1,"This is an emergency, who do you want to call?\n> ",0x31,0,0);
  FUN_0040101d(0,0,&DAT_00404000,8,0,0);
  FUN_0040101d(1,1,"What is your emergency?\n> ",0x1a,0,0);
  FUN_0040101d(0,0,local_28,0x80,0,0);
  return 0;
}
```
La funzione  **FUN_0040101d** fa una chiamata alla funzione **_syscall()_** di C. Il **primo** parametro (destinato al **registro** della CPU $rax) indica il codice della syscall (0 = **_sys_read_**, 1 = **_sys_write_**), il **secondo** (destinato a $rsi) indica il canale di comunicazione (1 = **_standard output_**, 2 = **_standard input_**), il **terzo** (destinato a $rdi) indica l'indirizzo del buffer in memoria (da dove leggere o dove scrivere), infine il **quarto** indica la dimensione massima in **byte** del dato da leggere/scrivere. Gli ultimi parametri sono impostati a 0 perchè le chiamate a **_sys_write_** e **_sys_read_** non richiedono ulteriori parametri. 
Vediamo che la variabile **_local_28_** è stata dichiarata per contenere **32 byte** (1 carattere corrisponde ad un byte), ma l'ultima lettura legge fino a **80 byte**. Questo significa che c'è una vulnerabilita di **buffer overflow**, che si può sfruttare per un attacco **ROP** (Return-Oriented-Programming) per chiamare la syscall **execve** per eseguire la shell di comando.
## 3. Exploitation
L'obiettivo è avviare la shell di comando tramite una syscall ad **execve**. Sfruttiamo il **buffer overflow** per eseguire un attacco **ROP**. Tramite il **buffer overflow** andiamo a sovrascrivere lo **stack**, in modo da inserire sulla cima, che viene segnata dal registro **$rsp** (stack pointer), l'indirizzo di memoria dell'inizio della **catena** di **gadget** che andiamo ad iniettare. In questo modo quell'indirizzo, a cui punta $rsp, verrà messo in $rip (instruction pointer), che contiene l'indirizzo di memoria dell'istruzione successiva, ingannando così il processo.
Per capire che **payload** iniettare per inserire l'inizio della catena esattamente sulla cima dello stack si può calcolare, tramite un pattern, un **offset**. Per fare ciò è sufficiente usare **gdb**, inserire il comando `pattern create num_bytes` (es: pattern create 80) e poi, una volta che il programma è andato in **segmentation fault**, utilizzare il comando `pattern offset $rip`, che restituirà l'offset (in questo caso 40), che indica il numero di bytes che ci sono prima di sovrascrivere il registro. 
E' necessario trovare anche gli indirizzi dei **gadget** disponibili da utilizzare all'interno del programma. Per trovarli tutti quanti si può utilizzare lo strumento **ROPgadget** con il comando `ROPgadget --binary ./emergency-call`
Abbiamo tutti gli strumenti necessari per eseguire l'attacco, ma prima serve la stringa _bin/sh_ come parametro per **execve** per avviare la shell. Ma per fare ciò basta inserirla come input alla prima richiesta del programma, perchè sappiamo esattamente l'indirizzo in cui verrà salvata.

Di seguito il link al codice dell'exploit:
[Codice exploit](rop.py)

Ecco la flag ottenuta:
```
flag{Th3_b35T_em3Rg3nCy_C4ll_1s_Sy5c411!}
```