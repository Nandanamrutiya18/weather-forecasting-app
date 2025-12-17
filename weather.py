import requests
from tkinter import *
from datetime import datetime

# ------------------ Weather Fetch Function ------------------
def get_weather():
    api_key = ""YOUR_API_KEY" "  # Replace with Your Weather forcasting API Key 
    city = city_entry.get().strip()

    if not city or city.lower() == "enter city name":
        temperature_label.config(text="Enter city name", fg="#ff4b2b")
        description_label.config(text="", fg="#333")
        wind_label.config(text="")
        humidity_label.config(text="")
        pressure_label.config(text="")
        card_frame.config(bg="white")
        return

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": "metric"}

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if data.get("cod") == 401:
            temperature_label.config(text="Invalid API Key", fg="#ff4b2b")
            description_label.config(text="Check your OpenWeatherMap API key", fg="#333")
            wind_label.config(text="")
            humidity_label.config(text="")
            pressure_label.config(text="")
            card_frame.config(bg="white")
            return

        if data.get("cod") == "404":
            temperature_label.config(text="City not found", fg="#ff4b2b")
            description_label.config(text="Please check the city spelling", fg="#333")
            wind_label.config(text="")
            humidity_label.config(text="")
            pressure_label.config(text="")
            card_frame.config(bg="white")
            return

        if response.status_code == 200:
            main = data["main"]
            wind = data["wind"]
            weather = data["weather"][0]

            temperature = main["temp"]
            feels_like = main["feels_like"]
            pressure = main["pressure"]
            humidity = main["humidity"]
            wind_speed = wind["speed"]
            description = weather["description"]

            current_time = datetime.now().strftime("%I:%M %p")

            # Update UI with professional colors
            temperature_label.config(text=f"{temperature}°C", fg="#ff4b2b")
            description_label.config(text=f"{description.capitalize()} | Feels like {feels_like}°C", fg="#333")
            wind_label.config(text=f"🌬 Wind: {wind_speed} m/s", fg="#0072ff")
            humidity_label.config(text=f"💧 Humidity: {humidity}%", fg="#00c6ff")
            pressure_label.config(text=f"⚡ Pressure: {pressure} hPa", fg="#ff7e5f")
            time_label.config(text=current_time, fg="#555")

            # Change card background slightly to highlight
            card_frame.config(bg="#e0f7fa")

        else:
            temperature_label.config(text="Error fetching data", fg="#ff4b2b")
            description_label.config(text=data.get("message", ""), fg="#333")
            wind_label.config(text="")
            humidity_label.config(text="")
            pressure_label.config(text="")
            card_frame.config(bg="white")

    except requests.exceptions.RequestException as e:
        temperature_label.config(text="Network error", fg="#ff4b2b")
        description_label.config(text=str(e), fg="#333")
        wind_label.config(text="")
        humidity_label.config(text="")
        pressure_label.config(text="")
        card_frame.config(bg="white")

# ------------------ GUI ------------------
root = Tk()
root.title("Weather Forecast App")
root.geometry("600x550")
root.configure(bg="#cceeff")
root.resizable(True, True)

# ------------------ Card Frame with Blue Border ------------------
card_frame = Frame(root, bg="white", bd=3, relief=RIDGE,
                   highlightbackground="#0072ff", highlightcolor="#0072ff", highlightthickness=3)
card_frame.place(relx=0.03, rely=0.03, relwidth=0.94, relheight=0.94)

# ------------------ City Entry with Blue Border ------------------
city_entry = Entry(card_frame, font=("Helvetica", 16, "bold"), justify="center",
                   fg="#aaa", bd=2, relief=GROOVE,
                   highlightthickness=2, highlightbackground="#0072ff", highlightcolor="#0072ff")
city_entry.insert(0, "Enter city name")
city_entry.pack(pady=20, ipadx=10, ipady=5)

def on_entry_click(event):
    if city_entry.get() == "Enter city name":
        city_entry.delete(0, "end")
        city_entry.config(fg="black")

def on_focusout(event):
    if city_entry.get() == "":
        city_entry.insert(0, "Enter city name")
        city_entry.config(fg="#aaa")

city_entry.bind('<FocusIn>', on_entry_click)
city_entry.bind('<FocusOut>', on_focusout)

# ------------------ Search Button ------------------
get_button = Button(card_frame, text="Get Weather", font=("Helvetica", 14, "bold"),
                    bg="#0072ff", fg="white", activebackground="#005ea2", activeforeground="white",
                    bd=0, relief=RIDGE, command=get_weather)
get_button.pack(pady=10, ipadx=10, ipady=5)

# ------------------ Time Label ------------------
time_label = Label(card_frame, font=("Helvetica", 12), bg="white")
time_label.pack()

# ------------------ Temperature Label ------------------
temperature_label = Label(card_frame, font=("Helvetica", 44, "bold"), bg="white")
temperature_label.pack(pady=10)

# ------------------ Weather Description Label ------------------
description_label = Label(card_frame, font=("Helvetica", 14), bg="white")
description_label.pack(pady=5)

# ------------------ Details Frame ------------------
details_frame = Frame(card_frame, bg="white")
details_frame.pack(pady=15)

wind_label = Label(details_frame, font=("Helvetica", 12), bg="white")
wind_label.grid(row=0, column=0, padx=25)

humidity_label = Label(details_frame, font=("Helvetica", 12), bg="white")
humidity_label.grid(row=0, column=1, padx=25)

pressure_label = Label(details_frame, font=("Helvetica", 12), bg="white")
pressure_label.grid(row=0, column=2, padx=25)

# ------------------ Footer ------------------
footer_label = Label(card_frame, text="Weather App by Nandan", font=("Helvetica", 10), bg="white", fg="#555")
footer_label.pack(side=BOTTOM, pady=5)

root.mainloop()
