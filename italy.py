def regionIT(var):
    if var == "Piedmont":
        state_IT = "Piemonte"
    if var == "Lombardy":
        state_IT = "Lombardia"
    if var == "Veneto":
        state_IT = "Veneto"
    if var == "Aosta Valley":
        state_IT = "Valle d'Aosta"
    if var == "Trentino-South Tyrol":
        state_IT = "P.A. Bolzano P.A. Trento"
    if var == "Tuscany":
        state_IT = "Toscana"
    if var == "Sicily":
        state_IT = "Sicilia"
    if var == "Apulia":
        state_IT = "Puglia"
    if var == "Friuli–Venezia Giulia":
        state_IT = "Friuli Venezia Giulia"
    else:
        state_IT = var
    return state_IT
