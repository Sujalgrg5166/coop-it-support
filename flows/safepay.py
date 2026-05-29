flow = {
    "start": {
        "question": "Er SafePay slukket før rengøring?",
        "yes": "open_coin_unit",
        "no": "turn_off_power"
    },

    "turn_off_power": {
        "question": "Sluk for strømmen til SafePay på ON/OFF knappen eller tag strømstikket ud. Tryk Ja, når du har gjort det.",
        "yes": "open_coin_unit",
        "no": "turn_off_power"
    },

    "open_coin_unit": {
        "question": "Er møntdelen åbnet korrekt?",
        "yes": "clean_rotor",
        "no": "open_correctly"
    },

    "open_correctly": {
        "question": "Åbn møntdelen ved at tage fat i udbetalingsskålen eller siderne af mønttårnet og træk mod dig selv. Tryk Ja, når den er åbnet.",
        "yes": "clean_rotor",
        "no": "open_correctly"
    },

    "clean_rotor": {
        "question": "Blæs rent rundt i hele rotordelen. Er rotordelen rengjort?",
        "image": "safepay_rotor.png",
        "yes": "open_validator",
        "no": "clean_rotor_instruction"
    },

    "clean_rotor_instruction": {
        "question": "Rengør rotordelen med trykluft og tør efter med en fnugfri klud. Husk at holde trykluften lodret og lave knæk på plastikrøret. Tryk Ja, når du er færdig.",
        "image": "safepay_rotor.png",
        "yes": "open_validator",
        "no": "clean_rotor_instruction"
    },

    "open_validator": {
        "question": "Har du trykket på reject-knappen bagpå møntenheden, så lågen åbner?",
        "image": "safepay_reject_button.png",
        "yes": "clean_coin_sensors",
        "no": "open_validator_instruction"
    },

    "open_validator_instruction": {
        "question": "Tryk på reject-knappen bagpå møntenheden, så lågen på møntvalideringen åbner. Tryk Ja, når lågen er åben.",
        "image": "safepay_reject_button.png",
        "yes": "clean_coin_sensors",
        "no": "open_validator_instruction"
    },

    "clean_coin_sensors": {
        "question": "Er møntslisken og sensorerne rengjort?",
        "image": "safepay_coin_sensors.png",
        "yes": "done",
        "no": "clean_sensor_instruction"
    },

    "clean_sensor_instruction": {
        "question": "Blæs sensorerne rene med trykluft og rengør med fnugfri klud eller en blød tandbørste. Brug ikke væsker. Tryk Ja, når området er rengjort.",
        "image": "safepay_coin_sensors.png",
        "yes": "done",
        "no": "clean_sensor_instruction"
    },

    "done": {
          "question": "Virker SafePay korrekt nu efter rengøringen?",
    "yes": "success",
    "no": "contact_support"
},

"success": {
    "solution": "Perfekt — SafePay fungerer nu korrekt igen."
},

"contact_support": {
    "solution": "Problemet er stadig ikke løst. Kontakt venligst COOP IT Servicedesk for videre support."
}
}