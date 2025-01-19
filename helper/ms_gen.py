import random

class ReactionMessage:
    def __init__(self):
        self.messages = [
            "Alors, toi qui es toujours aussi curieux, tu as lu jusqu'ici ! Maintenant, pourquoi ne pas ajouter une petite réaction sur les vidéos juste au-dessus ? Ça prend deux secondes, et ça fait plaisir ! 🔥",
            "Si tu as pris le temps de lire ce message, pourquoi ne pas montrer un peu d’amour en réagissant aux vidéos ci-dessus ? Un petit geste qui ne coûte rien mais qui fait la différence ! 😌",
            "J’imagine que tu es arrivé jusqu'ici, alors laisse une petite réaction sur les vidéos ci-dessus, ça nous aide tous à rendre l’expérience encore plus fun ! 💥",
            "Tu sais, ta curiosité m’impressionne toujours ! Et si tu laissais maintenant une petite réaction sur les vidéos en haut ? C’est rapide et ça met de l’ambiance ! 🎉",
            "Bon, maintenant que tu as lu ce message, je t’invite à ajouter une réaction sur les vidéos au-dessus ! Un petit pouce, une émoticône, tout ce que tu veux ! 😄",
            "Tu as l'air bien curieux ! Alors, après avoir lu ce message, n'oublie pas de réagir aux vidéos juste au-dessus, ça serait vraiment top ! 👏",
            "Eh bien, félicitations, tu es arrivé jusqu’ici ! Si ça te dit, laisse une réaction sur les vidéos au-dessus, c'est un geste simple mais super sympa ! 😊",
            "Maintenant que tu es là, pourquoi ne pas participer en ajoutant une petite réaction sur les vidéos ci-dessus ? C’est facile, et c’est toujours apprécié ! ✨",
            "Tu veux vraiment marquer ta curiosité ? Alors n’hésite pas à réagir aux vidéos au-dessus, c’est une façon cool de montrer ton intérêt ! 😎",
            "Si tu as pris une minute pour lire ce message, laisse une petite réaction sur les vidéos juste au-dessus, merci d'avance ! 🙏"
            "Tu peut me crée plusieurs petite phrase de ce genre : Ta curiosité m’épatera toujours, je voulu juste que tu lise ce message et comme tu l’a lu laisse des petits reactions sur les vidéos ci haut stp 😮‍💨",
            "Tu es vraiment imprévisible, j'espère que tu as pris le temps de lire ce message. Maintenant, laisse des petites réactions sur les vidéos au-dessus, ça fait toujours plaisir ! 😏",
            "Ta curiosité n'a pas de limites ! J'avais juste envie que tu lises ce message, et si tu l'as fait, laisse une petite réaction sur les vidéos en haut, ça serait super ! 👀",
            "Alors, tu as lu ce message, maintenant pourquoi ne pas réagir aux vidéos au-dessus ? C'est super simple, et c'est toujours apprécié ! 😍",
            "Tu n’arrêtes jamais de me surprendre ! Si tu es arrivé jusqu'ici, laisse une petite réaction sur les vidéos du dessus, ça ne coûte rien ! 😎",
            "Toujours aussi curieux ! J'espère que tu as bien lu ce message, maintenant n'oublie pas de réagir aux vidéos en haut, c'est rapide et sympa ! 😉",
            "Tu es vraiment un vrai curieux, j'adore ça ! Alors, après avoir lu ce message, laisse une petite réaction sur les vidéos ci-dessus, ça fait chaud au cœur ! ❤️",
            "Toujours là à explorer chaque détail ! Si tu as lu ce message, laisse une petite réaction sur les vidéos ci-dessus, c'est tout simple ! 👏",
            "J'adore ton esprit curieux, tu me surprends toujours ! Allez, maintenant laisse une petite réaction sur les vidéos en haut, juste pour le fun ! 😜",
            "Tu es toujours aussi curieux, et c’est ce que j'aime ! Maintenant que tu as lu ce message, pense à laisser une petite réaction sur les vidéos juste au-dessus, s'il te plaît ! 😊",
            "Ta curiosité est sans fin, je t’admire ! Maintenant que tu as lu ce message, pense à laisser une petite réaction sur les vidéos ci-dessus, ça me ferait plaisir ! ✨",
            "Tu es vraiment insatiable ! Après avoir lu ce message, laisse une petite réaction sur les vidéos en haut, c’est rapide et ça fait toujours plaisir ! 😁",
            "Toujours aussi attentif, j'adore ! Maintenant que tu es ici, laisse une petite réaction sur les vidéos du dessus, ça serait génial ! 🤩",
            "Ta soif de savoir est impressionnante ! Alors, si tu as bien lu ce message, pense à réagir aux vidéos en haut, c'est un petit geste mais ça fait toute la différence ! 🫣",
            "J’adore ta curiosité, tu n’en as jamais assez ! Après avoir lu ce message, pense à mettre une petite réaction sur les vidéos ci-dessus, ça serait top ! 🫶",
            "Toujours prêt à découvrir, c’est ce que j’aime chez toi ! Alors, après avoir lu ce message, laisse une petite réaction sur les vidéos au-dessus, c’est rapide ! 🙌",
            "Tu me surprends à chaque fois avec ta curiosité ! Si tu as lu ce message, laisse une petite réaction sur les vidéos du dessus, ça ne coûte rien et ça fait plaisir ! 💬",
            "Un esprit curieux comme le tien mérite d’être encouragé ! Si tu as pris le temps de lire ce message, n’oublie pas de laisser une petite réaction sur les vidéos ci-dessus, ça serait super ! 🔥",
            "Ta curiosité n'a vraiment pas de limite, j'adore ça ! Maintenant que tu es là, laisse une petite réaction sur les vidéos du dessus, c’est un petit geste mais précieux ! 🎉",
            "Toujours aussi curieux, tu es incorrigible ! Si tu as bien lu ce message, laisse une petite réaction sur les vidéos ci-dessus, c’est tout simple ! 😄",
            "T'es toujours là à explorer ! Alors, après avoir lu ce message, laisse une petite réaction sur les vidéos du dessus, ça fait plaisir à tout le monde ! 🥳",
            "On dirait que ta curiosité est infinie ! Si tu as pris une minute pour lire ce message, laisse une petite réaction sur les vidéos juste au-dessus, merci d'avance ! 🙏",
            "Alors, toi qui es toujours aussi curieux, tu as lu jusqu'ici ! Maintenant, pourquoi ne pas ajouter une petite réaction sur les vidéos juste au-dessus ? Ça prend deux secondes, et ça fait plaisir ! 🔥",
            "Si tu as pris le temps de lire ce message, pourquoi ne pas montrer un peu d’amour en réagissant aux vidéos ci-dessus ? Un petit geste qui ne coûte rien mais qui fait la différence ! 😌",
            "J’imagine que tu es arrivé jusqu'ici, alors laisse une petite réaction sur les vidéos ci-dessus, ça nous aide tous à rendre l’expérience encore plus fun ! 💥",
            "Tu sais, ta curiosité m’impressionne toujours ! Et si tu laissais maintenant une petite réaction sur les vidéos en haut ? C’est rapide et ça met de l’ambiance ! 🎉",
            "Bon, maintenant que tu as lu ce message, je t’invite à ajouter une réaction sur les vidéos au-dessus ! Un petit pouce, une émoticône, tout ce que tu veux ! 😄",
            "Tu as l'air bien curieux ! Alors, après avoir lu ce message, n'oublie pas de réagir aux vidéos juste au-dessus, ça serait vraiment top ! 👏",
            "Et voilà, tu as tout lu ! Maintenant, à ton tour d’agir : laisse une petite réaction sur les vidéos ci-dessus et montre-nous ce que tu penses ! 😉",
            "Eh bien, félicitations, tu es arrivé jusqu’ici ! Si ça te dit, laisse une réaction sur les vidéos au-dessus, c'est un geste simple mais super sympa ! 😊",
            "Maintenant que tu es là, pourquoi ne pas participer en ajoutant une petite réaction sur les vidéos ci-dessus ? C’est facile, et c’est toujours apprécié ! ✨",
            "Tu veux vraiment marquer ta curiosité ? Alors n’hésite pas à réagir aux vidéos au-dessus, c’est une façon cool de montrer ton intérêt ! 😎",
            "Un peu de curiosite ne fait pas de mal, likes les message ci dessus et tu pourras voir comment les autres réagissent ! 😉"
        ]
    
    def get_random_message(self):
        return random.choice(self.messages)

# Exemple d'utilisation
message_generator = ReactionMessage()
print(message_generator.get_random_message())
