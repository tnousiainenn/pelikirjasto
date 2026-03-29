# Pelikirjasto

* Sovelluksessa käyttäjät pystyvät jakamaan pelien kuvauksia. Kuvauksissa lukee pelin nimi ja sisältö.
* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
* Käyttäjä pystyy lisäämään pelien kuvauksia ja muokkaamaan ja poistamaan niitä.
* Käyttäjä näkee sovellukseen lisätyt pelit/pelien kuvaukset.
* Käyttäjä pystyy etsimään pelejä/pelien kuvauksia hakusanalla.
* Käyttäjäsivu näyttää, montako pelien kuvausta käyttäjä on lisännyt ja listan käyttäjän lisäämistä pelien kuvauksista.
* Käyttäjä pystyy valitsemaan pelille yhden tai useamman luokittelun (esim. tasohyppely, fps, seikkailu, jne.).
* Käyttäjä pystyy antamaan pelille kommentin ja arvosanan. Pelistä näytetään kommentit ja keskimääräinen arvosana.

# Ohjeet käyttämiseen

* 1. Lataa tiedostot ja laita ne samaan hakemistoon
* 2. Avaa komentoikkuna ja siirry hakemistoon, jossa sovellus on (esim. jos laitat sovelluksen hakemistoon "pelikirjasto" aja komento "cd pelikirjasto")
* 3. Kun olet oikeassa hakemistossa, aja komento "python3 -m venv venv" luodaksesi hakemistoon virtuaaliympäristön
* 4. Aktivoi virtuaaliympäristö komennolla "source venv/bin/activate"
* 5. Aja komento "pip install flask"
* 6. Aja komento "sqlite3 database.db"
* 7. Aja sqlite3 tilassa "schema.sql" tiedostossa olevat tietokantakomennot ja sen jälkeen aja komento ".quit"
* 8. Varmista että olet venv-tilassa ja aja komento "flask run"
* 9. Mene selaimessa osoitteeseen "http://127.0.0.1:5000"
* 10. Sovelluksen pitäisi olla nyt käynnissä testausta varten :)

