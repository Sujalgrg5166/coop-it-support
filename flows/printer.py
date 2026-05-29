flow = {
    "start": {
        "question": "Er printeren tændt?",
        "yes": "check_paper",
        "no": "turn_on_printer"
    },

    "check_paper": {
        "question": "Er der papir i printeren?",
        "yes": "restart_printer",
        "no": "add_paper"
    },

    "turn_on_printer": {
        "solution": "Tænd printeren og prøv igen."
    },

    "add_paper": {
        "solution": "Læg papir i printeren og prøv igen."
    },

    "restart_printer": {
        "solution": "Genstart printeren og prøv igen."
    }
}