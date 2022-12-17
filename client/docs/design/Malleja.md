# Hahmotelma malleista

- MVC-rakenne
  - Malliluokkia
    - Ruutu
    - Kenttä
    - Pelaaja
  - Näkymäluokkia
    - Pelinäkymä -> riippuu pelattavasta pelistä
    - Odotusnäkymä -> ei riipu pelistä
    - Matchmakingin pyytämisen näkymä -> ei riipu pelistä
    - Pelin lopun näkymä
      -> Pääsy takaisin Matchmakingin pyytämisen näkymään
  - Kontrollerit
    - Pelilogiikka