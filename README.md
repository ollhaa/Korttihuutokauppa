<h2> KORTTIHUUTOKAUPPA </h2>

<h3> YLEISTÄ </h3>

Korttihuutokauppa on nettihuutokauppasovellus, jossa on mahdollista tarjota huudettavaksi urheilukortteja, kuten jääkiekkokortteja. Tarjoaja asettaa kortin tyypin lisäksi, paikkakunnan, kunnon, aloitushinnan ja päättymispäivän. Lisäksi tarjoajan on asettava otsikko ja kuvaus kortista sekä laitettava kaksi kuvaa kortista. 

Potentiaalinen ostaja voi hakea aktiivisia huutokauppoja paikkakunnan, kortin tyypin ja kunnon perusteella ja tehdä korotuksia sekä lähettää palautetta. Admin-oikeuksilla oleva käyttäjä voi antaa admin oikeuksia ja lähettää viestejä muille käyttäjille. 

<h3> OHJEET </h3>

Kloonaa repositorio koneellesi ja siirry sen juurikansioon. Tämän jälkeen luo .env-tiedosto ja lisää sinne seuraaava: 

`DATABASE_URL=<tietokannan-paikallinen-osoite>` \
`SECRET_KEY=<salainen-avain>`

Seuraavaksi sinun täytyy aktivoida virtuaaliympäristö ja asentaa välttämättömät riippuvuudet:

`$ python3 -m venv venv` \
`$ source venv/bin/activate` \
`$ pip install -r ./requirements.txt`

Tämän jälkeen määrittele tietokantataulut:

`$ psql < schema.sql`

Lopulta pääset käynnistämään ohjelman komennolla:

`$ flask run`

Admin-oikeudet ovat käyttäjällä Admin. Salasana on adminword.

<h3> TOIMINNOT </h3>

 * Uusi käyttäjä voi rekisteröityä sovellukseen
 * Rekisteröitynyt käyttäjä voi kirjatua sovellukseen sisään ja ulos sovelluksesta
 * Sisäänkirjautunut käyttäjä voi luoda uuden huutokaupan
 * Sisäänkirjatunut käyttäjä voi hakea aktiivisia huutokauppoja kortin tyypi, paikkakunnan ja kortin kunnon perusteella
 * Sisäänkirjautunut käyttäjä voi tehdä korotuksen aktiivisena olevaan huutokauppaan
 * Sisäänkirjatunut käyttäjä voi vaihtaa salasanansa
 * Sisäänkirjatunut käyttäjä voi lähettää palautetta sovelluksesta
 * Sisäänkirjautunut käyttäjä voi lukea saamiaan viestejä
 * Admin-käyttäjä voi lähettää viestejä muille käyttäjille
 * Admin-käyttäjä voi antaa admin-oikeudet toiselle käyttäjälle
 * Admin-käyttäjä voi päivittää huutokaupat (päättäminen, voittajan selvittäminen ja viestit) 

<h3> NÄKYMÄT </h3>

 * Rekisteröinti (Register)
 * Tietoa (About)
 * Kirjatuminen (Login)
 * Etusivu ()
 * Uusi huutokauppa (New)
 * Haku (Search)
 * Huutokauppa (Auction id_: riippuu huutokaupan tiedoista)
 * Profiili (Profile)
 * Viestit (Messages)
 * Anna palautetta (Feedback)
 * Ylläpitäjä (Admin: vaatii admin-oikeudet)

<h3> TAULUT </h3>

 * users
 * auctions
 * images
 * feedbacks
 * bids
 * messages

<h3> PARANNUSEHDOTUKSET </h3>

 * Palautteiden lukeminen ei onnistu tällä hetkellä sovelluskesssa
 * Huutokauppojen muokkaaminen saattaisi olla hyvä toiminto käyttäjälle (kirjoitusvirheet yms.)
 * Automaattiset viestit kerran päivässä tms. voittajille ei onnistu tällä hetkellä
 * Autommaattiset huutokauppojen sulkemiset, kun aikaraja tulee täyteen ei onnistu tällä hetkellä
 * Testausta on tehty vain manuaalisesti
 * Graafinen ulkoasu voisi olla paljon parempi. 
 * Osa toiminnoista, kuten viestit ja niiden lukeminen, ovat hieman köpelösti tehtyjä.


<h3> MUUTA </h3>

Ohjelma toimii hyvin. En löytänyt manuaalisella testaamisella virheitä. Ajatus on automatisoida päättyneiden huutokauppojen päivittämiset, mutta en saanut tätä toimimaan. Ohjelmaa voisi laajentaa parannusehdotusten pohjalta melko helposti. 
