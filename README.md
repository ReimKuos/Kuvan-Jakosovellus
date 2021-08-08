# Kuvien jako sovellus

!https://calm-bayou-52457.herokuapp.com/

## Kuvaus

Sovellus on medianjako sovellus jossa voidaan jakaa kuvia ja keskustella niistä.

Ominaisuuksia:

 - Kuvien jakamiseen liittyen
    - Kuvien jakaminen tapahtuu ryhmissä
    - Kuvan jakamisen yhteydessä sille annetaan otsikko
    - kuka tahansa joka näkee kuvan voi kommentoida sitä
        - myös kommentteja voi kommentoida

 - Ryhmiin liittyen
    - Kuka tahansa voi aloittaa uuden ryhmän
    - Ryhmän luoja saa automaattisesti hallitsija oikeudet luotuun ryhmään, jotka hän voi jakaa muille halutuille käyttäjille
        - Hallitsija oikeudet omaava voi poistaa ryhmästä minkä tahansa kuvan/kommentin
        - Hallitsija oikuden omaava voi poistaa ryhmästä kenetkä tahansa, minkä jälkeen poistettu ei voi nähdä ryhmän kuvia/ kommentteja
    - Ryhmä voi olla joko avoin, jolloin se näkyy kaikille käyttäjille tai suljettu, jolloin se näkyy ja sinne pääsevät vain henkilöt, jotka hallitsija ryhmään hallitsija oikeudet sinne päästää

 - Käyttäjiin liittyen
    - Käyttäjä voi kirjautua ulos/sisään 
    - Kuvien jakaminen vaatii käyttäjä tunnuksen
    - Jokaisella käyttäjällä on nimike sekä tunnus, nimikkeen ei tarvitse olla uniikki, mutta tunnuksen tarvitsee olla
 
 - "Selaaminen"
    - Ryhmiä ja kuvia voi hakea eri parametrien suhteen, esimerkiksi niiden julkaisu ajan, kommenttien tai suosion perusteella (todennäköisesti jonkin näköisen "like/dislike" järjestelmän avulla)
    - Selata voi myös ilman käyttäjä tunnusta 

## Tämän hetkinen toiminnallisuus

- Käyttäjä tunnuksen voi luoda
- Ryhmän voi luoda
- kuvia voi laittaa ryhmiin

## Puutteellisuus

- !!!Mitään ei voi poistaa!!!
- Error checking ja input feedback toimintoja ei ole
