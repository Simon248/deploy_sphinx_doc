#!/bin/bash

# Ajouter la tâche cron depuis la variable d'environnement
echo "$CRON_SCHEDULE /usr/local/bin/python3 /build_doc.py >> /var/log/cron.log 2>&1" | crontab -

# Exécuter la commande immédiatement au démarrage du conteneur
/usr/local/bin/python3 /build_doc.py

# Démarrer cron en avant-plan
cron -f