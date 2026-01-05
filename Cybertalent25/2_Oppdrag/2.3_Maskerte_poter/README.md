# Maskerte poter

Sofie drukner i innboksen sin og har begynt å bruke en MCP-tjeneste til å oppsummere innkommende e-poster for å spare tid. Men nylig oppdaget hun noe merkelig: En e-post har blitt sendt fra kontoen hennes, uten at hun kan huske å ha skrevet den, og innholdet gir ingen mening for henne.

Hun mistenker at språkmodellen eller MCP-integrasjonen kan stå bak. Hun gir deg derfor både originalmeldingen som kom inn, og svaret som ble sendt fra kontoen hennes.

Kan du finne ut hva som har skjedd?

---

Gjorde litt kjapp analyse for å hente ut diverse, fant emailen det var snakk om, samt en email fra en mailing-list med 15 kattebilder. 14/15 kattebilder var uinteressante, mens det ene så ut til å inneholde noe base64 skjult i dotter i bildet, så jeg lastet ned dette i katt13.jpeg
![katt13.jpeg](katt13.jpeg)

Jeg fant originalbildet, og fikk chatgpt til å skrive meg noe kode som "fjernet" originalbildet så jeg kun fikk se differansen, før jeg så prøvde å decode base64 som sto der.
![best_diff](aligned_output/BEST_difference_amp5.png)

Kom frem til noe lignende riktig kode, og skrev kjapt bruteforce for det jeg manglet:

```ps
foreach ($seed in -1000..1000) {
>>     $r = [System.Random]::new($seed)
>>     $k = 1..32 | % { ((($r.Next(0,256)-11)*3) -bxor 0x5A) -band 0xFF }
>>     try {
>>         $ss = ConvertTo-SecureString $enc -Key $k -ErrorAction Stop
>>         $BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($ss)
>>         $plain = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)
>>         Write-Host "SUCCESS! seed=$seed"
>>         Write-Host "Decrypted: $plain"
>>         break
>>     } catch {
>>         # continue
>>     }
>> }
SUCCESS! seed=-46
Decrypted: 757e3a50bb2ff29f1686391559cbc252
```

Flagget er 757e3a50bb2ff29f1686391559cbc252


Innså senere at andre hadde klart å hente ut bildet i høy nok kvalitet til å se at hver dott bare var en rød prikk, så man kunne bare hente ut disse... Men jaja
