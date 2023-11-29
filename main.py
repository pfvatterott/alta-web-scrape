from ski_history_scraper import SkiHistory

ski_history = SkiHistory()
ski_history.login()
ski_history.enter_web_id()
total_ft_and_days = ski_history.get_ski_history()

# Yearly Totals
total_days = total_ft_and_days.text.split("SKIED: ")[1]
total_ft = total_ft_and_days.text.split("TOTAL VERTICAL FEET ")[1].split(", NUMBER")[0]
average_ft_per_day = int(total_ft.replace(",", "")) / int(total_days)

day_list = ski_history.get_each_day()
    
# Runs Each Day
day_list = ski_history.get_runs_each_day(day_list)
print(day_list)
            
        