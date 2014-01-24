# -*- coding: utf-8 -*-


# graph_names = ['nMembres', 'nSp_spInstant', 'nGM_nSp', 'GM', 'niv', 'player', 'player_sp', 'player_ea', 'player_df']


class GraphsMetaDataStore:
    def __init__(self):
        self.leg = {}
        # self.title = {}
        self.init()
        
    def init(self):
        self.leg['nMembres'] = u'Nombre de membres dans la CoGM'
        self.leg['nSp_spInstant'] = u'Cumul des pf dépensés (en jaune) et pf dépensés a chaque augmentation de GM (en bleu)'
        self.leg['nGM_nSp'] = u'Cumul des pf dépensés (en bleu) et Cumul du nombre d’augmentations de GM (en rouge)'
        self.leg['GM'] = u'Quel type de GM a le plus souvent été augmenté par la CoGM ?'
        self.leg['niv'] = u'Quel niveau de GM a le plus souvent été augmenté par la CoGM ?'
        self.leg['player'] = u'Quel membre de la CoGM a vu ses GM être augmentés le plus souvent ?'
        self.leg['player_sp'] = u'pf dépensés par les membres.'
        self.leg['player_ea'] = u'pf recus par les membres.'
        self.leg['player_df'] = u'Solde de membres (Solde = dépenses – recettes).'
        