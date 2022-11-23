# Hahmotelma viesteistä, jotka liittyvät clienttiin

## Jonoonasettumisnäkymässä

* jonoon asettuminen -> lähetetään tieto matchmakerille, vaihdetaan näkymä
* pelin alku -> vastaanotetaan tieto matchmakeriltä, siirrytään pelinäkymään

## Pelinäkymä

* siirron vastaanottaminen -> päivitetään tila, lähetetään vahvistus
* siirron lähettäminen -> lähetetään kaikille
* pelin loppu -> lähetetään tieto matchmakerille, siirrytään Pelin lopun näkymään
* ajan loppuminen -> lähetetään tieto matchmakerille, siirrytään Pelin lopun näkymään

## Pelin lopun näkymä

Ei viestejä, painikkeella takaisin Jonoonasettumisnäkymään