from asyncio import run
from datetime import datetime, timedelta
from random import choices, randint
from uuid import uuid4

from loguru import logger

from common import connect_db
from dog_repository import DogsCRUD
from model import Dog


def get_random_dog_names(locale: str, n_names: int = 1):
    if locale.lower() == 'mexico':
        mexican_dog_names = [
            "Alejandro", "Ángel", "Antonio", "Arturo", "Carlos", "Coco",
            "Diego", "Eduardo", "Fernando", "Francisco",
            "Gerardo", "Adriana", "Alejandra", "Alicia", "Ana María",
            "Araceli", "Carmen", "Elena", "Elizabeth",
            "Esmeralda",
            "Frida", "Gloria", "Guadalupe", "Isabel", "Josefina", "Juana",
            "Leticia", "Lola", "Luisa", "María",
            "Maya", "Nina", "Rosa", "Selena", "Silvia", "Teresa", "Verónica",
            "Yolanda",
            "Alba", "Alma", "Amiga", "Amigo", "Amor", "Bella", "Churro",
            "Corazón", "Luna", "Mariposa",
            "Sol", "Valeria", "Xiomara", "Andrés", "Azul", "Beso", "Blanco",
            "Chico", "Diablo", "El Perro",
            "Felipe", "Feliz", "Fernando", "Fido", "Gordito", "Javier",
            "Luis Mi", "Monarch", "Pedro",
            "Queso", "Salsa", "Taco", "Tajin", "Tamale", "Tequila",
            "Tocino", "Tortilla",
            "Tostito", "Ximena", "Acapulco", "Cancun", "Chichén Itzá",
            "Cozumel",
            "Durango", "Guadalajara", "Isla Mujeres", "Mazatlán",
            "Mérida", "Oaxaca", "Palenque",
            "Puerto Vallarta",
            "Puebla",
            "Tulum",
            'Chema',
            'Golfo',
            'Indio',
            'Jarocho',
            'Moneterrey',
            'Pibil',
            'Tabasco',
            'Tepic',
            'Todos Santos'
        ]
        names = mexican_dog_names
    elif 'korea' in locale.lower():
        korean_dog_names = [
            "Dak-Ho", "Geon", "Ho-Seok", "Hwan", "Jae-Hee", "Jong-Seok",
            "Kyu",
            "Min-ho", "Seo-Jin", "Seulgi",
            "Seung", "Suk", "Su-won", "Tae-Hui", "U-Yeong", "Yeo", "Yu-Jin",
            "Ae-Cha", "Bae", "Bo-mi", "Bong Cha",
            "Choon-Hee", "Danbi", "Eui", "Eun", "Gaeul", "Hae", "Ha-eun",
            "Hea",
            "Hye", "In-na", "Ji-a", "Kwan",
            "Mee", "Nam-Sun", "Seok-Yeong", "So-Hui", "Sung", "Ye-Jin",
            "Yu-na",
            "Gae", "Gang-aji", "Sanyang-gae",
            "Jagiya", "Yeobo", "Aein", "Aegiya", "Naekkeo", "Gwiyomi",
            "Nae sarang", "Wangjanim", "Gongjunim", "Oppa",
            "Yeojachingu", "Namjachingu", "Chin", "Cho", "Chun", "Dae",
            "Dong",
            "Gi", "Haneul", "Hee", "Hei", "Ho",
            "Hyun", "Iseul", "Ja", "Ji", "Jin", "Jung", "Kyong", "Min",
            "Moon",
            "Myung", "Ryung", "Sang", "Shin",
            "Soo", "Woong", "Yon", "Yong", "Anjong", "Bada", "Bong",
            "Bonhwa",
            "Cho", "Chungae", "Daehim", "Dal",
            "Haenguni", "Haru", "Him", "Hyeon", "Hyeri", "Jiho", "Minjun",
            "Miso", "Namjachingu", "Namu", "Nuri",
            "Seongbin", "Seulgi", "Suwon", "Uyeong", "Unmyeong", "Wangjanim"
        ]
        names = korean_dog_names
    else:
        italian_dog_names = [
            "Aba", "Abe", "Achille", "Ada", "Adamo", "Ade", "Ado", "Adolfo",
            "Agar", "Agata", "Ago", "Alaska", "Alan",
            "Alba", "Alberto", "Alcatraz", "Alco", "Alfredo", "Aika", "Alfa",
            "Alice", "Amadeus", "Amata", "Amato",
            "Ambra", "Amanda", "Amelia", "America", "Amedeo", "Amigo", "Amor",
            "Anita", "Andromeda", "Apollo",
            "Arianna", "Arancione", "Argo", "Arlena", "Arlette", "Arturo",
            "Arminia", "Artù", "Asia", "Asterisco",
            "Asso", "Astro", "Atena", "Atos", "Attila", "Aurora", "Azzurra",
            "Baffy", "Baffo", "Baldo", "Bambola",
            "Banko", "Baronessa", "Barbina", "Bamia", "Baramia", "Barica",
            "Bartolomeo", "Battista", "Bea", "Bella",
            "Biscotti", "Cannoli", "Caprese", "Cappuccino", "Dante", "Dolce",
            "Enzo", "Fabio", "Ferrari", "Gianna",
            "Giuseppe", "Guido", "Isabella", "Luigi", "Luna", "Maria", "Rocco",
            "Romeo", "Valentina", "Vita", "Angelo",
            "Bruno", "Giacomo", "Gino", "Michelangelo", "Paolo", "Paisano",
            "Valentino", "Vito", "Alessandria",
            "Amalfi", "Calabria", "Casoria", "Catania", "Lazio", "Milan",
            "Naples", "Palermo", "Pisa", "Pompeii",
            "Sicily", "Siena", "Tivoli", "Tuscany", "Venice", "Armani",
            "Caesar", "Cicero", "Dante", "Enzo", "Fabio",
            "Ferrari", "Galileo", "Lamborghini", "Leonardo", "Marco",
            "Maserati", "Michelangelo", "Pavarotti", "Polo",
            "Raphael", "Biscotti", "Cannoli", "Caprese", "Cappuccino",
            "Espresso", "Gelato", "Linguine", "Meatball",
            "Nutella", "Pesto", "Scampi", "Tiramisu", "Vino"
        ]
        names = italian_dog_names

    return choices(names, k=n_names)


def get_random_lineages(n_lineages: int = 1):
    dog_lineages = [
        "French Bulldogs", "Labrador Retrievers", "Golden Retrievers",
        "German Shepherd Dogs", "Poodles",
        "Bulldogs", "Rottweilers", "Beagles", "Dachshunds",
        "German Shorthaired Pointers",
        "Pembroke Welsh Corgis", "Australian Shepherds", "Yorkshire Terriers",
        "Cavalier King Charles Spaniels",
        "Doberman Pinschers", "Boxers", "Miniature Schnauzers",
        "Cane Corso", "Great Danes", "Shih Tzu",
        "Siberian Huskies", "Bernese Mountain Dogs",
        "Pomeranians", "Boston Terriers", "Havanese",
        "English Springer Spaniels", "Shetland Sheepdogs",
        "Brittanys", "Cocker Spaniels", "Border Collies",
        "Miniature American Shepherds", "Belgian Malinois",
        "Vizslas", "Chihuahuas", "Pugs",
        "American Staffordshire Terriers", "Boxers (Boxer)",
    ]
    return choices(dog_lineages, k=n_lineages)


def get_random_birthdates(max_age_days: int, n_dates: int = 1):
    today = datetime.now().date()
    dates = [today - timedelta(days=randint(1, max_age_days))
             for _ in range(n_dates)]
    return dates


async def main():
    N = 10
    names = get_random_dog_names(locale='north korea', n_names=N)
    lineages = get_random_lineages(n_lineages=N)
    bdates = get_random_birthdates(max_age_days=7 * 360, n_dates=N)

    random_dogs = [Dog(id=uuid4(), breed_id=uuid4(), lineage=lineage,
                       birthdate=bdate, name=name)
                   for (lineage, bdate, name) in zip(lineages, bdates, names)]
    print(random_dogs)

    # inicjalizacja polaczenia z baza
    DATABASE_URL = 'postgres://postgres:postgres@10.10.1.200:5432/postgres'
    # protocol :// user : password @ host : port / name_of_db
    pool = await connect_db(DATABASE_URL)
    print('db connected')
    repo = DogsCRUD(pool=pool)

    # zapis losowych psow
    for dog in random_dogs:
        logger.info(f'Creating dog with name: {dog.name}')
        await repo.create_dog(dog)


if __name__ == '__main__':
    run(main())
