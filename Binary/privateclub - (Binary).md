---
titolo: "Write-up: privateclub - (Binary)"
data: 2026-09-24
categoria: Binary
tags:
  - overflow
  - scanf
---
## 1. Informazioni Generali
* **Piattaforma:** [olicyber.training.it]
* **Sezione:** [Software Security]
* **Difficoltà:** [Facile]
* **Sfida:** `nc privateclub.challs.olicyber.it 10015`
## 2. Allegati
In allegato alla sfida viene fornito l'eseguibile del programma C che gira sul server
## 3. Analisi delle vulnerabilità
Analizzando il file con **Ghidra** e andando sulla funzione main possiamo leggere questo:
```C
undefined8 main(EVP_PKEY_CTX *param_1)

{
  undefined name [32];  //il nome delle variabili name ed age sono stati
						//modificati a seguito
  uint age;
  char local_14;
  
  init(param_1);
  local_14 = '\0';
  puts("Quanti anni hai?");
  __isoc99_scanf(&DAT_00402019,&age);
  puts("Come ti chiami?");
  __isoc99_scanf(&DAT_0040202c,name);
  if (local_14 == '\0') {
    puts("Non hai il badge, mi dispiace.");
  }
  else {
    printf("Ciao %s, bentornato :)\n",name);
    printf("Hai %d anni.\n",(ulong)age);
    system("/bin/sh");
  }
  return 0;
}
```
Vediamo che c'è una condizione **if** che controlla il valore di **_local14_** e fa passare nel ramo **else** (che è quello che ci interessa perchè ci fa accedere alla shell) solo se è diversa da **\0**. Il problema è che viene impostata a quel valore all'inizio della funzione **main**.
Si vede che la variabile **_name_** è un array di grandezza 32 di tipo **_char_** (dato che il programma chiede di inserire il proprio nome). Il suo valore viene impostato tramite uno **scanf**, ma andando a controllare cosa contiene la stringa all'indirizzo **_&DAT_0040202c_** (sempre tramite Ghidra), vediamo che il suo valore è **_%s_**, andando a confermare che non è stato fatto un controllo per prevenire il **Buffer Overflow** (in questo caso specifico **Stack-based Buffer Overflow**).
## 4. Exploitation
Sfruttando il **Buffer Overflow** della variabile **_name_** è possibile andare a sovrascrivere l'area di memoria di **_local_14_**, raggirando quindi il controllo dell'if e accendendo alla shell.
Prima di tutto, quando il programma chiede il nome si invia una stringa più lunga di 32 caratteri (che è il massimo che può contenere **_name_**), così si attiva la **shell**.
Ora eseguendo il comando `ls` si legge che c'è un file chiamato **_flag_**. Ci basta quindi digitare `cat flag` e si trova così la flag:
```
flag{b4d_sc4nf}
```