#!/bin/bash

#nettoyer la variable d'env CRON_SCHEDULE
CLEAN_CRON_SCHEDULE=$(echo "$CRON_SCHEDULE" | sed 's/[^a-zA-Z0-9* /]*//g')

# Ajouter la tâche cron depuis la variable d'environnement
echo "$CLEAN_CRON_SCHEDULE /usr/local/bin/python3 /build_doc.py >> /var/log/cron.log 2>&1" | crontab -

# Exécuter la commande immédiatement au démarrage du conteneur
/usr/local/bin/python3 /build_doc.py

# Démarrer cron en avant-plan
cron -f
