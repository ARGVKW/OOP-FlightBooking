from model.BelfoldiJarat import BelfoldiJarat
from model.Legitarsasag import Legitarsasag
from model.NemzetkoziJarat import NemzetkoziJarat

legitarsasagok = [
    Legitarsasag("Luft Panda", [
        NemzetkoziJarat(1, "Kuala Lumpur", 1200.00, 120),
        BelfoldiJarat(2, "Debrecen", 250.00, 60)
    ])
]

print(str(legitarsasagok))
