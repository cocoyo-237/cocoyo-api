# Schéma Supabase - projet collaborateur (`tzvovursbwvzejobmxpt`)

Source de vérité **en production** pour ce workspace (introspection directe Postgres).

## Tables

| Table | Rôle |
| ------- | ------ |
| `articles` | Catalogue (prix vente/achat, stock, couleurs) |
| `clients` | Clients (`nom`, `prenom`, `telephone`, …) |
| `commandes` | Commandes + statuts paiement/livraison |
| `lignes_commande` | Lignes panier |
| `profiles` | Profil gérant / boutique |

Les modèles ORM sont dans `infrastructure/database/models/`.

## MCP Cursor (option B)

Le MCP Supabase du compte Cursor actuel ne liste pas ce projet. Pour l’inspecter via MCP :

1. Se connecter au compte Supabase qui possède `tzvovursbwvzejobmxpt`
2. Reconfigurer l’intégration Supabase dans Cursor
3. Vérifier avec `list_tables` sur le schéma `public`

## Migration repo

`supabase/migrations/00001_initial_schema.sql` décrit un schéma **anglais** (legacy plan) - **non appliqué** sur le projet collaborateur. Référence alignée : `00002_collaborator_schema_reference.sql`.
