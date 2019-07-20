import csv
from requests_html import HTML
import re
import copy

input_html_file = "input.html"
output_csv_file = "output.csv"

csv_file = open(output_csv_file, "w", encoding="utf-8", newline='')
csv_writer = csv.writer(csv_file)

with open(input_html_file, encoding="utf-8") as html_file:
    source = html_file.read()
    html = HTML(html=source)

first_messages = html.find('.pam', first=True)
participants = re.split(', |: | et ', first_messages.text)
del (participants[0])

csv_writer.writerow(["date", "auteur", "message"] + participants + ["Vrai message"])

base_reac = []
for p in participants:
    base_reac.append(0)

def extract_reaction(text):
    reac = copy.copy(base_reac)

    splitted_text = text.text.split('\n')
    nb_of_reac = 0
    for elt in splitted_text:
        for i, auteur in enumerate(participants):
            if auteur in elt and "@" not in elt and len(auteur) + 1 == len(elt):
                nb_of_reac += 1
                reac[i] = elt[0]
    return reac, ''.join(splitted_text[:-1 * nb_of_reac])


non_human_generated_sequences = ["a envoyé une pièce jointe",
                                 "a envoyé un lien",
                                 "a créé un sondage",
                                 "a voté pour «",
                                 "a nommé le groupe ",
                                 "a défini l’emoji sur",
                                 "a surnommé",
                                 "a défini votre pseudo sur",
                                 "Vous avez défini l’emoji sur",
                                 "Vous avez ajouté",
                                 "Vous avez envoyé un lien",
                                 "Vous avez quitté le groupe",
                                 "Vous avez choisi le pseudo",
                                 "Vous avez défini le pseudo de",
                                 "Vous avez changé la photo du groupe",
                                 "Vous avez nommé le groupe",
                                 "modifié les couleurs de la discussion",
                                 "rejoint la discussion vidéo",
                                 "Vous avez voté pour «",
                                 "Vous avez marqué",
                                 "a battu son record personnel de",
                                 "a répondu Participe",
                                 "a gagné des places dans le leaderboard",
                                 "a battu son record personnel",
                                 "occupe la première position",
                                 "vous a défié(e) à",
                                 "Discussion vidéo terminée.",
                                 "a commencé à partager une vidéo",
                                 "a rejoint l’appel",
                                 "a démarré un appel.",
                                 "a envoyé une position",
                                 "Vous avez battu votre record personnel",
                                 "a retiré son vote pour «",
                                 "a supprimé le nom du groupe",
                                 "a défini l’emoji sur",
                                 "a effacé son propre pseudo.",
                                 "a défini son propre pseudo sur",
                                 "https://",
                                 "http://",
                                 "a changé la photo du groupe.",
                                 "a ajouté",
                                 "a quitté le groupe.",
                                 "a défini votre pseudo sur",
                                 " /!\ Media file /!\ ",
                                 "Vous avez répondu",
                                 "Télécharger le fichier :",
                                 "a mis à jour le plan",
                                 "turned on auto-translation",
                                 "turned off auto-translation",
                                 "a répondu Ne participe pas",
                                 "vient de jouer. C’est à votre tour !",
                                 "a joué, maintenant c’est votre tour !",
                                 " a le record de",
                                 "est maintenant à la 1ère place",
                                 "a réalisé son meilleur score",
                                 "a commencé un plan.",
                                 "a remplacé le nom du plan par",
                                 "a remplacé le lieu du plan par",
                                 " a modifié son vote pour «",
                                 " imgur.com",
                                 "@dailycute",
                                 "Swelly : Score of",
                                 "to move (White)",
                                 "to move (Black)",
                                 "no text",
                                 "@fbchess",
                                 "a démarré une discussion",
                                 "L’appel est terminé.",
                                 "a remplacé le lieu du plan",
                                 "terminée, voir les résultats maintenant !",
                                 "C’est votre tour !",
                                 "La discussion vidéo est terminée.",
                                 " a supprimé le pseudo de",
                                 "a supprimé votre",
                                 "a retiré la photo de groupe.",
                                 "a envoyé un sticker",
                                 "Vous occupez la première place",
                                 "Vous avez gagné des places dans le leaderboard",
                                 "Vous avez démarré une discussion vidéo.",
                                 "Tasks :",
                                 "l’approbation des membres"]


def test_if_real_text(text):
    real = True

    for seq in non_human_generated_sequences:
        if seq in text:
            real = False

    if "a marqué" in text and " points" in text:
        real = False

    if "a marqué" in text and "à" in text:
        real = False

    if "a voté pour" in text and "dans le sondage" in text:
        real = False

    if "a retiré" in text and "du groupe" in text:
        real = False

    return real


messages = html.find('.pam')
for m in messages:

    date = m.find('._3-94', first=True)
    if date != None:
        csv_date = date.text.replace('\r', '  ').replace('\n', '  ')
    else:
        continue

    auteur = m.find('._2pio', first=True)
    if auteur != None:
        csv_auteur = auteur.text.replace('\r', '').replace('\n', '')
    else:
        continue

    message_is_real_text = True
    text = m.find('._2let', first=True)
    if text != None:

        if "_2yuc" in text.html:
            csv_reac, _ = extract_reaction(text)
            csv_text = " /!\ Media file /!\ "

        elif "<li>" in text.html:
            csv_reac, csv_text = extract_reaction(text)

        else:
            csv_text = " ".join(text.text.split('\n'))
            csv_reac = base_reac
    else:
        csv_text = 'no text'
        csv_reac = base_reac

    message_is_real_text = test_if_real_text(csv_text)

    csv_writer.writerow([csv_date, csv_auteur, csv_text] + csv_reac + [message_is_real_text])

csv_file.close()
