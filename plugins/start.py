from pyrogram import filters,Client, enums
from pyrogram.types import Message
import traceback,time
from config import Config
LOG_CHANNEL = Config.LOG_CHANNEL
SUDO_USERS = Config.SUDO_USERS
import logging
LOGGER = logging.getLogger(__name__)
from utils.markup import empty_markup, start_markup,admin_markup
from database.models.user_db import add_user,get_admin

@Client.on_message(filters.command('start') & filters.private)
async def start_handler(bot : Client, message: Message):
    await bot.send_message(message.chat.id,"Bonjour **{}**".format(message.chat.first_name),parse_mode=enums.ParseMode.MARKDOWN,reply_markup=start_markup())
    await add_user(message)
    
@Client.on_message(filters.command('admin_start') & filters.private & filters.user(get_admin()))
async def admin_start_handler(bot : Client, message : Message):
    LOGGER.info(f"Admin logged in {message.chat.id}")
    await bot.send_message(message.chat.id,"✅ Vous êtes connecté en tant qu'administrateur",reply_markup=admin_markup())


@Client.on_callback_query(filters.regex('^back$'))
async def back_handler(bot : Client,message : Message):
    await bot.delete_messages(message.message.chat.id,message.message.id)
    
@Client.on_callback_query(filters.regex('^help$'))
async def help_handler(bot : Client, message : Message):
    help_text = """
    📢 **Aide - Promotions des Canaux et Services sur Telegram**

    Bienvenue dans l'assistance de votre service de promotion sur Telegram ! Ce service vous permet de promouvoir vos canaux et services en toute simplicité, tout en atteignant un large public.

    ✅ **Fonctionnalités principales :**

    1. **Promotions de Canaux** :
       - **Partage de messages promotionnels** avec vos abonnés.
       - **Accès à une large audience** via des groupes et canaux partenaires.
       - **Prommotion payante** pour des services spécifiques sur Telegram.

    2. **Services Promotionnels** :
       - **Publicité ciblée** pour des services spécifiques sur Telegram.
       - **Collaborations avec d'autres canaux** pour maximiser la visibilité.
       - **Personnalisation des campagnes** pour répondre à vos besoins.

    3. **Suivi des Statistiques** :
       - **Rapports détaillés** sur les performances des promotions.
       - **Analyse de l'engagement** des utilisateurs avec les campagnes.

    🚀 **Comment utiliser ce service ?**
       - Envoyer la CMD /start .
       - Ajoutez tout vos canaux.
       - Laissez-nous gérer la distribution et le suivi des résultats.

    Si vous avez des questions ou avez besoin d'assistance supplémentaire, n'hésitez pas à nous contacter ! Nous sommes là pour vous aider à maximiser l'impact de vos promotions sur Telegram.

    📬 **Contactez notre équipe de support** pour toute demande d'information complémentaire.

    """
    await bot.send_message(message.message.chat.id, help_text, reply_markup=empty_markup())

