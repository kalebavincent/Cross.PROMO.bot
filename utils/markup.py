from pyrogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from config import Config
from database.models.channel_db import get_all_channel
from database.models.post_db import get_buttons

PROMOTION_NAME = Config.PROMOTION_NAME
def start_markup():
    add_channel = InlineKeyboardButton('➕ Ajouter un canal', callback_data='add_channel')
    my_channel = InlineKeyboardButton('🏷 Mes canaux', callback_data='my_channel')
    share = InlineKeyboardButton('🌐 Partager le bot', switch_inline_query=' vous offre les meilleurs services de promotion croisée ! Ajoutez votre canal et participez aux promotions. Rejoignez maintenant {}'.format(PROMOTION_NAME))
    helpn = InlineKeyboardButton('🆘 Aide', callback_data='help')
    
    markup = InlineKeyboardMarkup(
        [
            [add_channel], [my_channel], [share, helpn]
        ]
    )
    return markup

def channel_markup():
    remove_channel = InlineKeyboardButton('🗑 Supprimer le canal', callback_data='remove_channel')
    markup = InlineKeyboardMarkup([[remove_channel]])
    return markup

def back_markup():
    cancel = KeyboardButton('🚫 Annuler')
    markup = ReplyKeyboardMarkup([[cancel]], resize_keyboard=True)
    return markup

def empty_markup():
    return ReplyKeyboardRemove()

async def remove_channel_markup(chat_id):
    channels = await get_all_channel(chat_id)

    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(x['channel_name'], callback_data=str(x['channel_id']))] for x in channels]
    )
def admin_markup():
    announce = InlineKeyboardButton('📢 Annonce', callback_data='announce')
    mail = InlineKeyboardButton('📤 Mailing', callback_data='mail')
    ban = InlineKeyboardButton('🚫 Bannir le canal', callback_data='ban')
    unban = InlineKeyboardButton('📍 Débannir le canal', callback_data='unban')
    update_subs = InlineKeyboardButton('🔄 Mettre à jour les abonnés', callback_data='update_subs')
    show_channel = InlineKeyboardButton('ℹ️ Infos du canal', callback_data='show_channel')
    manage = InlineKeyboardButton('📊 Statistiques', callback_data='stats')
    manage_list = InlineKeyboardButton('☑️ Gérer la liste', callback_data='list')
    create_post = InlineKeyboardButton('📝 Créer une publication', callback_data='create_post')
    preview_list = InlineKeyboardButton('⏮ Aperçu de la promo', callback_data='preview')
    send_promo = InlineKeyboardButton('✔️ Envoyer la promo', callback_data='send_promo')
    dlt_promo = InlineKeyboardButton('✖️ Supprimer la promo', callback_data='delete_promotion')
    task = InlineKeyboardButton('⚙️ Paramètres', callback_data='settings')
    add_admin = InlineKeyboardButton('🛠 Ajouter un admin', callback_data='add_admin')
    sendpaidpromo = InlineKeyboardButton('💲Envoyer promo payée', callback_data='send_paid_promo')
    deletepaidpromo = InlineKeyboardButton('💲Supprimer promo payée', callback_data='delete_paid_promo')
    markup = InlineKeyboardMarkup([[add_admin], [mail, announce], [ban, unban], [update_subs], [show_channel, manage_list], [manage, create_post], [preview_list, task], [send_promo, dlt_promo], [sendpaidpromo, deletepaidpromo]])
    return markup


def settings_markup():
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton('☑️ Définir la limite d\'abonnés', callback_data='subs_limit')],
            [InlineKeyboardButton('☑️ Définir la taille de la liste', callback_data='list_size')],
            [InlineKeyboardButton('☑️ Définir la taille de la grille', callback_data='grid_size')],
            [InlineKeyboardButton('🔙 Retour', callback_data='back')]
        ]
    )
    
def list_markup():
    channel_list = InlineKeyboardButton('🕹 Liste des canaux', callback_data='channel_list')
    ban_list = InlineKeyboardButton('🚫 Liste des bannis', callback_data='ban_list')
    user_list = InlineKeyboardButton('👤 Liste des utilisateurs', callback_data='user_list')
    back = InlineKeyboardButton('🔙 Retour', callback_data='back') 
    markup = InlineKeyboardMarkup([[channel_list, user_list], [ban_list], [back]])
    return markup


def create_post_markup():
    top_sponser = InlineKeyboardButton('⬆️ Définir le texte du haut', callback_data='set_top_text')
    bottom_sponser = InlineKeyboardButton('⬇️ Définir le texte du bas', callback_data='set_bottom_text')
    emoji = InlineKeyboardButton('☑️ Définir un emoji', callback_data='set_emoji')
    set_button = InlineKeyboardButton('🔘 Définir des boutons', callback_data='set_button')
    delete_button = InlineKeyboardButton('🗑 Supprimer des boutons', callback_data='delete_button')
    set_caption = InlineKeyboardButton('🔖 Définir la légende', callback_data='set_caption')
    add_image = InlineKeyboardButton('🖼 Ajouter une image', callback_data='add_image')
    back = InlineKeyboardButton('🔙 Retour', callback_data='back')
    markup = InlineKeyboardMarkup([[top_sponser, bottom_sponser], [emoji, set_caption], [set_button, delete_button], [add_image], [back]])
    return markup

def promo_button_markup():
    buttons = get_buttons()
    button = [[InlineKeyboardButton(x['name'], url=x['url']) for x in buttons]]
    markup = InlineKeyboardMarkup(button)
    return markup  

def preview_list_markup():
    button_promo = InlineKeyboardButton('🔳 Promo avec bouton', callback_data='preview_button_promo')
    classic_promo = InlineKeyboardButton('🏛 Promo classique', callback_data='preview_classic_promo')
    morden_promo = InlineKeyboardButton('🔰 Promo standard', callback_data='preview_morden_promo')
    descpromo = InlineKeyboardButton('🎐 Promo description', callback_data='preview_desc_promo')
    back = InlineKeyboardButton('🔙 Retour', callback_data='back')
    markup = InlineKeyboardMarkup([[button_promo, classic_promo], [morden_promo, descpromo], [back]])
    return markup

def announce_markup():
    open_reg = InlineKeyboardButton('📖 Ouvrir les inscriptions', callback_data='open_reg')
    close_reg = InlineKeyboardButton('📕 Fermer les inscriptions', callback_data='close_reg')
    list_out = InlineKeyboardButton('📰 Notification Liste', callback_data='list_out')
    back = InlineKeyboardButton('🔙 Retour', callback_data='back')
    markup = InlineKeyboardMarkup([[open_reg, close_reg], [list_out], [back]])
    return markup


def send_promo_markup():
    button_promo = InlineKeyboardButton('🔳 Promo avec bouton', callback_data='send_button_promo')
    classic_promo = InlineKeyboardButton('🏛 Promo classique', callback_data='send_classic_promo')
    morden_promo = InlineKeyboardButton('🔰 Promo standard', callback_data='send_standard_promo')
    descpromo = InlineKeyboardButton('🎐 Promo description', callback_data='send_desc_promo')
    back = InlineKeyboardButton('🔙 Retour', callback_data='back')
    markup = InlineKeyboardMarkup([[button_promo, classic_promo], [morden_promo, descpromo], [back]])
    return markup
