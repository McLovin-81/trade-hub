dax_aktien = {
    "SAP SE": "SAP.DE",
    "Siemens AG": "SIE.DE",
    "Deutsche Telekom AG": "DTE.DE",
    "Allianz SE": "ALV.DE",
    "Airbus SE": "AIR.DE",
    "Merck KGaA": "MRK.DE",
    "Mercedes-Benz Group AG": "MBG.DE",
    "Porsche AG": "P911.DE",
    "Münchener Rückversicherungs-Gesellschaft AG (Munich Re)": "MUV2.DE",
    "Siemens Healthineers AG": "SHL.DE",
    "BMW AG": "BMW.DE",
    "Volkswagen AG": "VOW3.DE",
    "Deutsche Post AG": "DPW.DE",
    "Infineon Technologies AG": "IFX.DE",
    "BASF SE": "BAS.DE",
    "Adidas AG": "ADS.DE",
    "Deutsche Börse AG": "DB1.DE",
    "E.ON SE": "EOAN.DE",
    "Henkel AG & Co. KGaA": "HEN3.DE",
    "Deutsche Bank AG": "DBK.DE",
    "Beiersdorf AG": "BEI.DE",
    "Delivery Hero SE": "DTG.DE",
    "Hannover Rück SE": "HNR1.DE",
    "Bayer AG": "BAYN.DE",
    "Vonovia SE": "VNA.DE",
    "RWE AG": "RWE.DE",
    "Rheinmetall AG": "RHM.DE",
    "Encavis AG": "ENR.DE",
    "HeidelbergCement AG": "HEI.DE",
    "Symrise AG": "SY1.DE"
}

def validate_and_find_symbol(user_input):
    """
    Validiert die Benutzereingabe und sucht nach dem entsprechenden Symbol.
    Gibt das gefundene Symbol zurück oder None, falls nicht gefunden.
    """
    # Benutzereingabe bereinigen
    user_input = user_input.strip().lower()
    
    # Leere Eingabe überprüfen
    if not user_input:
        return None
    
    # Suche im Dictionary nach dem Namen oder Symbol
    for name, symbol in dax_aktien.items():
        if user_input == name.lower() or user_input == symbol.lower():
            return symbol
    
    # Wenn keine Übereinstimmung gefunden wurde
    return None