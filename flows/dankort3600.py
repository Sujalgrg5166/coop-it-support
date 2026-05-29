flow = {
    "start": {
        "question": "Viser Dankort 3600 terminalen forbindelsessignal?",
        "yes": "restart_terminal",
        "no": "reconnect_ethernet"
    },

    "reconnect_ethernet": {
        "question": "Fjern ethernet-kablet fra terminalen og sæt det i igen. Viser terminalen forbindelsessignal nu?",
        "yes": "restart_terminal",
        "no": "power_restart"
    },

    "restart_terminal": {
        "question": "Tryk på COMMAND + CLEAR for at genstarte terminalen. Er terminalen genstartet?",
        "yes": "test_purchase",
        "no": "restart_terminal"
    },

    "test_purchase": {
        "question": "Lav et testkøb. Virker terminalen nu?",
        "yes": "success",
        "no": "power_restart"
    },

    "power_restart": {
        "question": "Sluk terminalen på hovedafbryderen. Fjern internetkablet fra væggen og sæt det i igen. Tænd terminalen igen. Viser skærmen 'NET OP'?",
        "yes": "success",
        "no": "contact_support"
    },

    "success": {
        "solution": "Dankort 3600 terminalen virker nu korrekt igen."
    },

    "contact_support": {
        "solution": "Problemet er ikke løst. Kontakt venligst COOP IT Servicedesk for videre support."
    }
}