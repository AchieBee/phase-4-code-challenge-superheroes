from app import app, db
from models import Power, Hero, Hero_Power
import random



def seed_powers():
  with app.app_context():
    powers_data = [
        {"name": "super strength", "description": "gives the wielder super-human strengths"},
        {"name": "flight", "description": "gives the wielder the ability to fly through the skies at supersonic speed"},
        {"name": "super human senses", "description": "allows the wielder to use her senses at a super-human level"},
        {"name": "elasticity", "description": "can stretch the human body to extreme lengths"}
    ]

    for data in powers_data:
        power = Power(**data)
        db.session.add(power)

def seed_heroes():
  with app.app_context():
    heroes_data = [
        {"name": "Kamala Khan", "super_name": "Ms. Marvel"},
        {"name": "Doreen Green", "super_name": "Squirrel Girl"},
        {"name": "Gwen Stacy", "super_name": "Spider-Gwen"},
        {"name": "Janet Van Dyne", "super_name": "The Wasp"},
        {"name": "Wanda Maximoff", "super_name": "Scarlet Witch"},
        {"name": "Carol Danvers", "super_name": "Captain Marvel"},
        {"name": "Jean Grey", "super_name": "Dark Phoenix"},
        {"name": "Ororo Munroe", "super_name": "Storm"},
        {"name": "Kitty Pryde", "super_name": "Shadowcat"},
        {"name": "Elektra Natchios", "super_name": "Elektra"}
    ]

    for data in heroes_data:
        hero = Hero(**data)
        db.session.add(hero)

def add_powers_to_heroes():
  with app.app_context():
    strengths = ["Strong", "Weak", "Average"]
    all_powers = Power.query.all()

    for hero in Hero.query.all():
        for _ in range(random.randint(1, 3)):
            power = random.choice(all_powers)
            strength = random.choice(strengths)
            hero_power = HeroPower(hero=hero, power=power, strength=strength)
            db.session.add(hero_power)

def main():
    print("🦸‍♀️ Seeding powers...")
    seed_powers()

    print("🦸‍♀️ Seeding heroes...")
    seed_heroes()

    print("🦸‍♀️ Adding powers to heroes...")
    add_powers_to_heroes()

    db.session.commit()
    print("🦸‍♀️ Done seeding!")

if __name__ == '__main__':
    main()
