import pandas as pd
import base64
import io
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')
from .models import UserActivityLog, Profile
from .models import Lab


def footfall():
    data = UserActivityLog.objects.values('user', 'login_time', 'logout_time')
    df = pd.DataFrame.from_records(data)

    def count_user(date, df): 
        start_date = pd.Timestamp(date).normalize()
        end_date = start_date + pd.Timedelta(days=1)
        return len(df[(df['login_time'] < end_date) & (df['logout_time'] >= start_date)])

    date_range = pd.date_range(df['login_time'].min().normalize(), df['logout_time'].max().normalize(), freq='D')

    footfall_per_day = [count_user(date, df) for date in date_range]

    plt.figure(figsize=(10, 6))
    plt.plot(date_range, footfall_per_day, label='Number of Users Logged In', color='blue')
    plt.fill_between(date_range, footfall_per_day, color='blue', alpha=0.1)
    plt.title('Footfall of the Website Per Day')
    plt.xlabel('Date')
    plt.ylabel('Number of Users')
    plt.legend()
    plt.tight_layout()
    plt.xticks(rotation=45)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    graph_url = base64.b64encode(buffer.read())
    buffer.close()

    return graph_url.decode('utf-8') 

def lab_footfall(admin):
    lab = Lab.objects.get(lab_admin=admin)
    data = UserActivityLog.objects.filter(user__profile__lab=lab)

    df = pd.DataFrame.from_records(data.values())

    def count_user(date, df): 
        start_date = pd.Timestamp(date).normalize()
        end_date = start_date + pd.Timedelta(days=1)
        return len(df[(df['login_time'] < end_date) & (df['logout_time'] >= start_date)])

    date_range = pd.date_range(df['login_time'].min().normalize(), df['logout_time'].max().normalize(), freq='D')

    footfall_per_day = [count_user(date, df) for date in date_range]

    plt.figure(figsize=(10, 6))
    plt.plot(date_range, footfall_per_day, label='Number of Users Logged In', color='blue')
    plt.fill_between(date_range, footfall_per_day, color='blue', alpha=0.1)
    plt.title(f'Footfall of Lab {lab.name} Per Day')
    plt.xlabel('Date')
    plt.ylabel('Number of Users')
    plt.legend()
    plt.tight_layout()
    plt.xticks(rotation=45)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    graph_url = base64.b64encode(buffer.read())
    buffer.close()

    return graph_url.decode('utf-8') 