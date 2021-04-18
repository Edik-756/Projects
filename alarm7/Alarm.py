from playsound import playsound
import datetime
import time
alarm_on = input("If you want to turn on the alarm, enter the 'yes': ").lower()
if alarm_on == 'yes':
    def alarm(hour, minute, second, n, sleep_min):
        while True:
            if hour == datetime.datetime.today().strftime("%H") \
                    and minute == datetime.datetime.today().strftime("%M") \
                    and second == datetime.datetime.today().strftime("%S"):
                print("WAKE UP!!!")
                for i in range(n):
                    playsound(r"C:\Users\Ed\Desktop\music\alarm.mp3")
                    if i == n - 1:
                        time.sleep(0)
                    else:
                        time.sleep(sleep_min)
                return 'Good Morning'


    time_hour = input("Enter the Hour: ")
    time_minute = input("Enter the Minute: ")
    time_second = input("Enter the Second: ")
    quantity_of_repeat = int(input("Enter quantity of repeat: "))
    minute_sleep = float(input("Enter how many minutes it will be repeated: ")) * 60
    result = alarm(time_hour, time_minute, time_second, quantity_of_repeat, minute_sleep)
    print(result)
