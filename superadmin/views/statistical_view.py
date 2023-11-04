import calendar
from rest_framework.response import Response
from rest_framework import status
from appwrite.services.users import Users
from datetime import datetime, timedelta
from collections import defaultdict
import re

from .base_view import BaseView
from synappgpt.module import *
from superadmin.constants.endpoints import *
from superadmin.constants.regex import *
from superadmin.wrappers.dot_notation_object import *

class StatisticalView(BaseView):
  def parse_data(self, data):
    day_data = defaultdict(int)
    iso_date_pattern = re.compile(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}')

    for entry in data:
      iso_date_match = iso_date_pattern.search(entry["created_at"])
      if iso_date_match:
          iso_date = iso_date_match.group()
          created_at = datetime.fromisoformat(iso_date)
          day_data[created_at.strftime("%Y-%m-%d")] += entry["count"]
    return day_data

  def calculate_weekly_stats(self, day_data):
    day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    week_data = {}
    current_date = start_of_week
    while current_date <= end_of_week:
      date_key = day_names[current_date.weekday()]
      week_data[date_key] = day_data.get(date_key, 0)
      current_date += timedelta(days=1)

    return week_data


  def calculate_monthly_stats(self, day_data):
    today = datetime.now()
    weekly_stats = defaultdict(int)
    current_month = today.month
    current_year = today.year
    current_week_number = today.strftime("%U")

    for i in range(1, int(current_week_number) + 1):
      week_start = today - timedelta(days=today.weekday(), weeks=i)
      week_end = week_start + timedelta(days=6)

      # Only include weeks that are in the current month and year
      if week_start.month == current_month and week_start.year == current_year:
          week_index = f"Week {i}"
          weekly_stats[week_index] += sum(day_data.get((week_start + timedelta(days=d)).strftime("%Y-%m-%d"), 0) for d in range(7))

    return weekly_stats

  def calculate_yearly_stats(self, day_data):
    today = datetime.now()
    yearly_stats = defaultdict(int)
    current_year = today.year
    for i in range(1, 13):
      month_key = today.replace(day=1, month=i).strftime("%B")[0:3]
      month_days = calendar.monthrange(current_year, i)[1]

      monthly_data = sum(
        day_data.get((today.replace(day=day, month=i)).strftime("%Y-%m-%d"), 0)
        for day in range(1, month_days + 1)
      )

      yearly_stats[month_key] = monthly_data

    return yearly_stats

  def get(self, request, format=None):
    result = super().list_documents('STATISTICAL_COLLECTION_ID')

    data = result['documents']
    day_data = self.parse_data(data)
    weekly_stats = self.calculate_weekly_stats(day_data)
    monthly_stats = self.calculate_monthly_stats(day_data)
    yearly_stats = self.calculate_yearly_stats(day_data)
    client = super().create_client()
    users = Users(client)

    result = users.list()

    return Response({'year':yearly_stats,'month':monthly_stats, 'weekly':weekly_stats, 'total_user':result['total']} ,status=status.HTTP_200_OK)
