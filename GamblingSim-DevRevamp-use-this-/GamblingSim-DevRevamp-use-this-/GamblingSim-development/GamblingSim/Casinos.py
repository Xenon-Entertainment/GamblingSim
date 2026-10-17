CASINOS = {
    "local": {
        "name": "Local Casino",
        "bet_limits": {
            "slot": 100,
            "blackjack": 500,
            "roulette": 500,
            "snap": 200,
            "coin_flip": 100,
        },
        "roulette_extra_zeros": 0,
        "blackjack_dealer_stand": 17,
        "slot_extra_symbols": 0,
        "coin_flip_player_win_probability": 0.50,
        "snap_dealer_speed": (1.2, 1.8),
        "job_pay_per_press": 10,
        "job_max_session_earnings": 200,
    },
    "high_roller": {
        "name": "High Roller Casino",
        "bet_limits": {
            "slot": 500,
            "blackjack": 1000,
            "roulette": 1000,
            "snap": 500,
            "coin_flip": 250,
        },
        "roulette_extra_zeros": 1,
        "blackjack_dealer_stand": 16,
        "slot_extra_symbols": 1,
        "coin_flip_player_win_probability": 0.48,
        "snap_dealer_speed": (1.0, 1.5),
        "job_pay_per_press": 15,
        "job_max_session_earnings": 300,
    },
    "vip": {
        "name": "VIP Casino",
        "bet_limits": {
            "slot": 2000,
            "blackjack": 1500,
            "roulette": 2000,
            "snap": 1000,
            "coin_flip": 500,
        },
        "roulette_extra_zeros": 2,
        "blackjack_dealer_stand": 15,
        "slot_extra_symbols": 2,
        "coin_flip_player_win_probability": 0.45,
        "snap_dealer_speed": (0.4, 1.2),
        "job_pay_per_press": 30,
        "job_max_session_earnings": 600,
    },
}

DEFAULT_CASINO = "local"
CASINO_UNLOCK_COSTS = {
    "high_roller": 2500,
    "vip": 10000,
}


def get_casino(tier=DEFAULT_CASINO):
    return CASINOS.get(tier, CASINOS[DEFAULT_CASINO])
