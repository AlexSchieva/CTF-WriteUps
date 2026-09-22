---
titolo: "Write-up: Intagram Generator - (Binary)"
data: 2026-09-24
categoria: Binary
tags:
  - out_of_bounds_read
---
## 1. Informazioni Generali
* **Piattaforma:** [olicyber.training.it]
* **Difficoltà:** [Facile]
* **Sfida:** `nc intagram.challs.olicyber.it 10101`
## 2. Allegati
La sfida dà in allegato il codice del programma, e un comando da inserire nel terminale per connettersi da remoto alla challenge (`nc intagram.challs.olicyber.it 10101`)
```C
// gcc -Wall -fno-stack-protector -o intagram_generator src.c

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void clear(){
    while(getchar() != '\n');
}

int main() {
  setvbuf(stdin, NULL, _IOLBF, 0);
  setvbuf(stdout, NULL, _IOLBF, 0);
  setvbuf(stderr, NULL, _IOLBF, 0);

  char frasi[10][64] = {
    "No Pain No Gain",
    "Non tutte le ciambelle escono col buco",
    "L’unica costante della vita è il cambiamento",
    "Dov'è Bugo?",
    "Il destino mescola le carte e noi giochiamo",
    "Non è tutto oro quel che luccica",
    "Il gioco è bello quando è bello",
    "Chi va a Roma perde la poltrona",
    "La vita è piena di sofferenza, ma almeno poi finisce",
    "Entro. Spacco. Esco. Ciao."
  };

  char system_strings[6][64] = {
    "Ritorna per nuove frasi d'effetto",
    "Ne desideri altre? (s/n)",
    "",
    "\nEcco qua la tua frase d'effetto:\n - %s\n\n",
    "Scegli un numero da 1 a 10 per avere la tua frase:\n> ",
    "Generatore frasi per Instagram v0.1",
  };

  FILE* f = fopen("flag", "r");
  fscanf(f, "%63s", system_strings[2]);
  fclose(f);

  unsigned short choice = 0;
  int index = 0;
  char endchoice;

  puts(system_strings[5]);

  do {
    int result = 0;
    do {
      printf(system_strings[4]);
      result = scanf("%hu", &choice);
      clear();
    } while(result != 1 || choice < 1);

    index = (int)(short) choice - 1;

    printf(system_strings[3], frasi[index]);

    do {
      puts(system_strings[1]);
      result = scanf("%c", &endchoice);
      clear();
    } while(result != 1);

  } while (endchoice == 's');

  puts(system_strings[0]);

}
```
## 2. Analisi delle vulnerabilità
Il programma chiede di inserire un numero da 1 a 10 per generare una frase. All'inizio del file contenente il codice C si vede un commento:
`// gcc -Wall -fno-stack-protector -o intagram_generator src.c`
Indica molto probabilmente come è stato compilato il programma, e si nota in particolare l'opzione **-fno-stack-protector**, che indica che è stata disabilitata l'opzione di sicurezza chiamata **_Stack Canary_**, che serve a rilevare ed evitare attacchi di **Buffer Overflow**. 
Analizzando ulteriormente il codice, notiamo che la **flag** viene presa da un file e caricata nell'array **_system_strings[2]_**. Osserviamo però la seguente porzione di codice: 
```C
unsigned short choice = 0;
int index = 0;

/*
...
...
*/
    
do {
    printf(system_strings[4]);
    result = scanf("%hu", &choice);
	clear();
} while(result != 1 || choice < 1);

index = (int)(short) choice - 1;

printf(system_strings[3], frasi[index]);
```
La variabile **_choice_** è di tipo **unsigned short**. Nel momento in cui passo un negativo alla funzione **scanf**, questo viene interpretato come un **unsigned short** (%hu): non sapendo come gestire il segno meno, lo interpreta come un numero positivo (ad esempio _-3_ lo converte in **65533**, perchè fa il giro (underflow)). Siccome **_choice_** è un numero positivo, il programma esce dal ciclo e si ritrova a fare un **cast** di choice a **short**. Il numero che prima era stato interpretato come numero positivo senza segno, ora viene interpretato come **short con segno**, quindi diventa, prendendo l'esempio di poco fa, **-3**. 
Nell'istruzione dopo, nella **printf**, verrà passato un indice **negativo** all'array **_frasi_**. In C questo comporta che dall'indirizzo di partenza di quell'array andrà a leggere in memoria ciò che è allocato prima di quell'array, facendo dei "salti" all'indietro. Ciò può essere sfruttato per leggere la flag che si trova nell'array allocato prima di **_frasi_**.
## 3. Exploitation
Quando il programma chiede di inserire un numero da 1 a 10, inserendo -3 viene letta la flag dall'array **_system_strings_** partendo dall'inizio dell'indirizzo di memoria di **_frasi_**. Infatti:
```
[ INDIRIZZI ALTI ] 
----------------------------------------- 
frasi[9] (Entro. Spacco...) 
... 
frasi[1] (Non tutte le ciambelle...) 
frasi[0] (No Pain No Gain) <-- La variabile "frasi" punta qui 
----------------------------------------- 
system_strings[5] (Generatore frasi...) <-- Equivalente a frasi[-1] system_strings[4] (Scegli un numero...) <-- Equivalente a frasi[-2] system_strings[3] (\nEcco qua la tua...) <-- Equivalente a frasi[-3] system_strings[2] ( IL CONTENUTO FLAG ) <-- Equivalente a frasi[-4] system_strings[1] (Ne desideri altre?...) 
system_strings[0] (Ritorna per nuove...) <-- La variabile "system_strings" punta qui 
----------------------------------------- 
[ INDIRIZZI BASSI ]
```
Ecco la flag ottenuta:
```
flag{w41t_th4ts_1ll3gal_c0m3_h41_f4tt0}
```