import requests

API_KEY = "5cad283173eed685ffc2640cfb631e2e"

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city},IN&appid={API_KEY}&units=metric"
    return requests.get(url).json()

def get_aqi(lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
    data = requests.get(url).json()
    return data["list"][0]["main"]["aqi"] if "list" in data else None

def calculate_risk(temp, weather, aqi):
    score = 0
    if weather.lower() == "rain": score += 2
    if temp > 40: score += 2
    if aqi and aqi >= 4: score += 2
    return "High" if score >= 4 else "Medium" if score >= 2 else "Low"

def calculate_premium(risk):
    return {"Low": 10, "Medium": 20, "High": 40}[risk]

def calculate_payout(weather, temp, income, aqi):
    if weather.lower() == "rain":
        return income, "Rain 🌧"
    if temp > 42:
        return income, "Heat 🌡"
    if aqi and aqi >= 5:
        return income, "Pollution 🌫"
    return 0, None

def workability_score(weather, temp, aqi):
    score = 100
    if weather.lower() == "rain": score -= 40
    if temp > 35: score -= 30
    if aqi and aqi >= 4: score -= 30
    return max(score, 0)