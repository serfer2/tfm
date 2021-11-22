HF_SITE_ID = 0

#  https://hackforums.net/forumdisplay.php?fid=<int>
HF_MARKET_SUBFORUMS_FID = {
    '163': 'Marketplace Discussions',
    '402': 'Promotional Advertising',
    '186': 'Free Services and Giveaways',
    '205': 'Appraisals and Pricing',
    '111': 'Deal Disputes',
    '107': 'Premium Sellers Section',
    '374': 'Premium Tools and Programs',
    '299': 'Cryptography and Encryption Market',
    '176': 'Secondary Sellers Market',
    '218': 'Virtual Game Items',
    '206': 'Member Auctions',
    '182': 'Currency Exchange',
    '291': 'Online Accounts',
    '309': 'Non-Free Accounts',
    '404': 'Adult Zone Accounts',
    '195': 'Gamertags',
    '136': 'Ebook Bazaar',
    '145': 'Hosting Services',
    '263': 'Social Media Services',
    '44': 'Buyers Bay',
    '225': 'Webmaster Marketplace',
    '106': 'Service Offerings',
    '219': 'Graphics Market',
    '171': 'VPN Hosting and Services',
    '308': 'Service Requests',
    '339': 'Hash Bounties',
    '217': 'Partnerships, Hiring, and Personnel',
    '255': 'Rewards and Small Favors',
}

CRAWLING_DIRECTION_FORWARD = 1
CRAWLING_DIRECTION_BACKWARD = 2

RELATED_TERMS = {
    'tech_terms': ('botnet', 'cryptostresser', 'ddos', 'mirai', 'stresser', 'webstresser'),
    'trade_terms': {
        'trade_terms_currency': (
            '£', '€', '$', '₽',
            'pound', 'euro', 'dollar', 'ruble',
            'pounds', 'euros', 'dollars', 'rubles',
            'bitcoin', 'ecoin', 'ethereum', 'litecoin',
            'btc', 'eth', 'ltc',
        ),
        'trade_terms_buy': (
            'wtb', 'buy', 'pay', 'market', 'paid', 'payment', 'price',
            'service', 'source',
        ),
        'trade_terms_sell': (
            'wts', 'payment', 'premium',
            'interkassa', 'paypal', 'perfectmoney',
            'price', 'sale', 'selling', 'selly',
            'service', 'shop', 'source', 'store', 'trusted',
        ),
    },
}
