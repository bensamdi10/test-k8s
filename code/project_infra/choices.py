# -*- coding: utf-8 -*-
PROVIDER = (
    ('Google_cloud', 'Google Cloud'),
    ('aws', 'AWS'),
    ('heroku', 'Heroku'),
    ('digital_ocean', 'Digital Ocean'),
    ('minikube', 'Minikube'),
)
TYPE_ENV = (
    ('developpement', 'Developpement'),
    ('test', 'test'),
    ('production', 'Production'),
    ('other', 'Other'),
)

TYPE_CONTAINER = (
    ('code_base', 'Code Base'),
    ('software', 'Software'),
    ('plugin', 'Add-ons / Plugin'),
    ('cron', 'Cron Job'),
    ('other', 'Other'),
)
TYPE_SERVICE = (
        ('travis', 'Travis CI'),
        ('gitlab', 'Gitlab'),
)
TYPE_TEMPLATE = (
    ('container', 'Container'),
    ('service', 'Service'),
    ('ingress', 'Ingress'),
    ('deployment', 'Deployment'),
    ('cluster_service', 'Cluster Service IP'),
    ('other', 'Other'),
)

ACCESS_MODE_VOLUME = (
    ('ReadWriteOnce', 'ReadWriteOnce'),
    ('ReadOnlyMany', 'ReadOnlyMany'),
    ('ReadWriteMany', 'ReadWriteMany '),
)
VOLUME_MODE = (
    ('Filesystem', 'Filesystem'),
    ('Blockdevice', 'Blockdevice'),
)

INGRESS_ANNOTATIONS = (
    ('ReadWriteOnce', 'ReadWriteOnce'),
    ('ReadOnlyMany', 'ReadOnlyMany'),
    ('ReadWriteMany', 'ReadWriteMany '),
)
VOLUME_TYPE = (
    ('persistent_volume', 'persistent_volume'),
    ('local_file_system', 'local_file_system'),
    ('container_volume', 'container_volume '),
)
CRON_TYPE = (
    ('cron', 'Cron'),
    ('job', 'Job'),
    ('deamon', 'Deamon '),
)
RESTART_POLICY = (
    ('OnFailure', 'OnFailure'),
    ('Never', 'Never'),
    ('always', 'always '),
)

TYPE_JOURNAL = (
    ('cron', 'cron'),
    ('import', 'Import'),
    ('config', 'config'),
    ('dailymail', 'dailymail'),
    ('schedule', 'schedule'),
)


COLORS = (
        ('#ffffff', 'White'),
        ('#000000', 'Black'),
        ('#e15554', 'rouge'),
        ('#107afe', 'bleu clair'),
        ('#ff4167', 'rose'),
        ('#2f2b9a', 'bleu violet'),
        ('#06abd8', 'bleu ciel'),
        ('#ffc400', 'yellow'),
        ('#63dd16', 'green'),
        ('#63dd16', 'green'),
        ('#b13f73', 'rose violet'),
        ('#ff8b66', 'orange'),
        ('#00e7b4', 'bleu tircoise'),
        ('#c1e732', 'green pistage'),
        ('#004818', 'green black'),
        ('#ff97a8', 'rose clair'),
        ('#a60002', 'red black'),
        ('#4c300b', 'orange black'),
)

STATUS = (
        ('pending', 'pending'),
        ('published', 'published'),
        ('spam', 'spam'),
        ('rejected', 'rejected'),
        ('error', 'error'),
        ('archived', 'archived'),
        ('draft', 'draft'),
)
EVENT_TYPE = (
        ('party', 'party'),
        ('conference', 'conference'),
        ('competition', 'competition'),
        ('promotion', 'promotion'),
        ('launching', 'launching'),

)
LAYOUT_ARTICLES = (
        ('standard', 'standard'),
        ('large', 'large'),
        ('text', 'text'),
        ('video', 'video'),
        ('product', 'product'),
)

SUPPORT = (
        ('game', 'game'),
        ('anime', 'anime'),
        ('manga', 'manga'),
        ('dvd', 'dvd'),
        ('book', 'book'),
)

TYPE = (
        ('article', 'article'),
        ('translate', 'translate'),
        ('event', 'event'),
        ('review', 'review'),
        ('test', 'test'),
        ('analyse', 'analyse'),
        ('list', 'list'),
        ('product', 'product'),
        ('video', 'video'),
        ('photo', 'photo'),
)

TYPE_ALERT = (
        ('alert', 'alert'),
        ('message', 'message'),
        ('info', 'info'),
)

LAYOUT_ALERT = (
        ('inline', 'inline'),
        ('popup', 'popup'),
        ('footer', 'footer'),
)

LAYOUT_CAROUSEL = (
        ('normal', 'normal'),
        ('loop', 'loop'),
        ('diaporama', 'diaporama'),
)

LAYOUTS = (
        ('block', 'block'),
        ('table', 'table'),
        ('list', 'list'),
        ('inline', 'inline'),
)
DEVISE = (
        ('mad', 'MAD'),
        ('euro', 'EURO'),
        ('usd', 'USD'),
        ('cad', 'CAD'),
)

STATUS_PRODUCT = (
        ('stock', 'in stock'),
        ('expired', 'expired'),
        ('subscribe', 'subscribe'),
)
TYPE_INBOX = (
        ('message', 'message'),
        ('response', 'response'),
)
STATUS_INBOX = (
        ('sent', 'sent'),
        ('read', 'read'),
        ('response', 'response'),
)
OWNER_INBOX = (
        ('user', 'user'),
        ('author', 'author'),
        ('platefome', 'platefome'),
)
TYPE_MEDIA = (
        ('image', 'image'),
        ('video', 'video'),
        ('audio', 'audio'),
        ('facebook', 'facebook'),
        ('twitter', 'twitter'),
        ('youtube', 'youtube'),
        ('iframe', 'iframe'),
)
TYPE_CREDIT = (
        ('standard', 'standard'),
        ('premium', 'premium'),
        ('special', 'special'),
)

TYPE_COMPOSANT = (
    ('article', 'article'),
    ('ad', 'ad'),
    ('author', 'author'),
    ('option', 'option'),
)
GENDER = (
        ('man', 'Man'),
        ('woman', 'Woman'),
        ('other', 'Other'),
    )
ROLES = (
        ('admin', 'Administrator'),
        ('manager', 'Manager'),
        ('internal-collaborator', 'Internal collaborator'),
        ('external-collaborator', 'External collaborator'),
        ('guest', 'Guest'),
    )

STATUS_PROFIL = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Invitation accepted', 'Invitation accepted'),
        ('Invitation pending', 'Invitation pending'),
)
TYPE_PROFIL = (
        ('user', 'user'),
        ('author', 'author'),
        ('translator', 'translator'),
        ('collaborator', 'collaborator'),
        ('employe', 'employe'),
        ('supervisor', 'supervisor'),
)
STATUS_TYPE_PROFIL = (
        ('user', 'user'),
        ('freelance', 'freelance'),
        ('collaborator_interne', 'collaborator_interne'),
        ('collaborator_externe', 'collaborator_externe'),
        ('partner', 'partner'),
)

TYPE_DESTINATION = (
        ('static', 'static'),
        ('dynamic', 'dynamic'),
)

TYPE_PAGE = (
        ('listing', 'listing'),
        ('details', 'details'),
        ('page', 'page'),
)
TYPE_WIDGET = (
        ('listing', 'listing'),
        ('preview', 'preview'),
)

TYPE_ELEMENT = (
        ('all', 'all'),
        ('section', 'section'),
        ('category', 'category'),
        ('topic', 'topic'),
        ('tag', 'tag'),
        ('article', 'article'),
        ('page', 'page'),
        ('video', 'video'),
        ('event', 'event'),

)

METRIC_ELEMENT = (
        ('last', 'last'),
        ('popular', 'popular'),
        ('tendance', 'tendance'),
        ('coming', 'coming'),
        ('comments', 'comments'),
        ('likes', 'likes'),
        ('views', 'views'),
        ('random', 'random'),

)

