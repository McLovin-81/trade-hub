def populate_products(db):

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
        "Deutsche Post AG": "DHL.DE",
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

    # Einträge in die Tabelle product einfügen
    for name, symbol in dax_aktien.items():
        db.execute("INSERT INTO product (symbol, name) VALUES (?, ?)", (symbol, name))
    db.commit()

def populate_status(db):
    stati ={
        0   : 'Ok',
        1   : 'Reset',
        2   : 'Delete'
    } 
    for id, description in stati.items():
        db.execute("INSERT INTO status (id, description) VALUES (?, ?)", (id, description))
    db.commit()