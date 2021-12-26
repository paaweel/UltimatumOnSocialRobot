# -*- encoding: UTF-8 -*-
"""
Prompts what to say during HRI.
"""
import qi
from config import Config


sentences = []

sentences.append("""Cześć, jestem Nao. Chcesz zagrać w grę Ultimatum?""")

# tak

sentences.append("""To wspaniale, wytłumaczyć Ci zasady gry?""")

# tak

sentences.append(
    """Wspólnie mamy dziesięć złotych. 
Za każdym razem musimy te pieniądze podzielić między siebie na dwie części tak, 
żeby każdy dostał przynajmniej jedną złotówkę. Będziemy zamieniać się rolami. 
Najpierw ja zaproponuję ile monet chcę zachować dla siebie, a Ty możesz tę propozycję przyjąć lub odrzucić. 
Jeśli zaakceptujesz mój pomysł to na twoim koncie znajdzie się zaproponowana przeze mnie kwota, a na Twoim pozostałe pieniądze. 
Jeśli go odrzucisz to oboje nie dostaniemy ani złotówki. 
Po zamianie ról Ty zaproponujesz ile złotych z nowej puli dziesięciu złotych chciałbyś zostawić dla siebie. 
Ja mogę tak samo zaakceptować lub odrzucić. Rozumiesz?"""
)

# tak

sentences.append(
    """okej, to ja zacznę! Proponuję 7 ziko dla Ciebie i 3 dla mnie, akceptujesz?"""
)

# tak

sentences.append("""definitywnie?""")

# definitywnie

sentences.append(
    """Super, oboje otrzymujemy ustaloną kwotę. Teraz Twoja kolej, jaki podział proponujesz?"""
)

# 6 dla Ciebie 4 dla mnie

sentences.append("""Pasuje mi taki podział, akceptuję""")
sentences.append("""Oboje dostajemy pieniądze""")

# super ekstra duper

sentences.append("""Dziękuję Ci za grę""")


def main():
    """
    Main entry point
    """

    session = qi.Session()
    try:
        session.connect("tcp://" + Config().ip)
        say_service = session.service("ALTextToSpeech")
        say_service.setLanguage(Config().language)
        s = raw_input()
        say_service.say(s)

    except RuntimeError:
        print("Can't connect to Nao at ip: " + Config().ip)
    except KeyboardInterrupt:
        print("Interruption received, shutting down")


if __name__ == "__main__":
    main()
