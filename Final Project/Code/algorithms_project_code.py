# -*- coding: utf-8 -*-
"""Algorithms_Project_Code.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jLgtVGcmmoc7x89tt40OaTJEFkf_txJc
"""

from datetime import datetime, timedelta
import matplotlib.pyplot as plt

job_priorities = {}

def calculate_priority(application, user_skills):
    # deadline_weight = 1.5
    preference_weight = 1.0
    skills_weight = 0.8
    experience_weight = 0.7
    reputation_weight = 0.6
    early_submission_bonus = 0.2
    education_weight = 0.5
    completeness_weight = 0.3
    recommendation_letters_weight = 0.4
    interview_performance_weight = 0.6
    location_preference_weight = 0.5
    diversity_weight = 0.3
    skill_match_threshold = 0.6

    days_left = (application['deadline'] - datetime.now()).days

    # Calculate the skills match factor based on user's skills and job application's required skills
    user_skills_set = set(user_skills)
    required_skills_set = set(application['required_skills'])
    skills_match = len(user_skills_set.intersection(required_skills_set)) / len(required_skills_set) if required_skills_set else 0

    # Define a dictionary to map education levels to numerical values
    education_level_values = {'PhD': 5, 'Master': 4, 'Bachelor': 3, 'High School': 2, 'Other': 1}

    # Convert education level to numerical value using the dictionary
    education_level_value = education_level_values.get(application['education_level'], 0)

    # Define a dictionary to map location preferences to numerical values
    location_preference_values = {'Urban': 5, 'Suburban': 4, 'Rural': 3}

    # Convert location preference to numerical value using the dictionary
    location_preference_value = location_preference_values.get(application['location_preference'], 0)

    priority = (
        # (deadline_weight * days_left) +
        (preference_weight * application['preference']) +
        (skills_weight * skills_match) +
        (experience_weight * application['experience']) +
        (reputation_weight * application['company_reputation']) +
        (early_submission_bonus / max(1, days_left)) +
        (education_weight * education_level_value) +
        (completeness_weight * application['completeness']) +
        (recommendation_letters_weight * application['recommendation_letters']) +
        (interview_performance_weight * application['interview_performance']) +
        (location_preference_weight * location_preference_value) +
        (diversity_weight * application['diversity_factor'])
    )

    job_priorities[application['job_id']] = priority
    return priority

def prioritize_applications(applications, user_skills):
    sorted_applications = sorted(applications, key=lambda app: calculate_priority(app, user_skills), reverse=True)
    return sorted_applications

def schedule_applications(prioritized_applications):
    current_time = datetime.now()
    schedule = []
    hm = {}
    calendar = {}
    x = {}
    threshold = 2
    d = current_time
    res = []
    missed_applications = []

    for application in prioritized_applications:
        days_until_deadline = (application['deadline'] - current_time + timedelta(days=1)).days
        hm[application['job_id']] = days_until_deadline

    # print(hm)

    for application in prioritized_applications:
        while d in x and x[d] >= threshold:
            d += timedelta(days=1)
        rem_days = (application['deadline'] - d).days
        if rem_days >= 0:
            calendar[application['job_id']] = d
            res.append({'job_id': application['job_id'], 'days_for_deadline': hm[application['job_id']],
                        'suggested_date': calendar[application['job_id']], 'priority': job_priorities[application['job_id']],
                        'company_name': application['company_name']})

            x[d] = 1 + x.get(d, 0)
        else:
            missed_applications.append({'job_id': application['job_id'], 'days_for_deadline': hm[application['job_id']],
                                 'priority': job_priorities[application['job_id']],'company_name': application['company_name']})

    return res, missed_applications

def plot_pie_chart(final_result):
    job_types_count = {}
    for application in final_result:
        job_type = job_applications[application['job_id'] - 1]['job_type']
        job_types_count[job_type] = job_types_count.get(job_type, 0) + 1

    labels = job_types_count.keys()
    sizes = job_types_count.values()

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.title("Number of Scheduled Applications by Job Type")
    plt.show()

if __name__ == "__main__":
    user_skills = ['Python', 'SQL', 'Communication', 'Machine Learning']

    job_applications = [
        {'job_id': 1, 'job_type': 'Software Engineer', 'deadline': datetime(2023, 12, 12), 'preference': 8, 'required_skills': ['Python', 'Java', 'SQL'], 'experience': 2, 'company_reputation': 0.8, 'education_level': 'Master', 'completeness': 0.9, 'recommendation_letters': 2, 'interview_performance': 0.8, 'location_preference': 'Urban', 'diversity_factor': 0.7, 'company_name': 'Alice'},
        {'job_id': 2, 'job_type': 'Data Scientist', 'deadline': datetime(2023, 12, 3), 'preference': 7, 'required_skills': ['Python', 'R', 'Machine Learning'], 'experience': 3, 'company_reputation': 0.9, 'education_level': 'PhD', 'completeness': 0.8, 'recommendation_letters': 1, 'interview_performance': 0.9, 'location_preference': 'Suburban', 'diversity_factor': 0.8, 'company_name': 'Bob'},
        {'job_id': 3, 'job_type': 'Product Manager', 'deadline': datetime(2023, 12, 3), 'preference': 9, 'required_skills': ['Product Management', 'Communication', 'Leadership'], 'experience': 4, 'company_reputation': 0.7, 'education_level': 'Bachelor', 'completeness': 0.7, 'recommendation_letters': 3, 'interview_performance': 0.7, 'location_preference': 'Rural', 'diversity_factor': 0.6, 'company_name': 'Charlie'}
        # {'job_id': 4, 'job_type': 'Data Scientist', 'deadline': datetime(2023, 12, 3), 'preference': 7, 'required_skills': ['Product Management', 'Communication', 'Leadership'], 'experience': 4, 'company_reputation': 0.7, 'education_level': 'Bachelor', 'completeness': 0.7, 'recommendation_letters': 3, 'interview_performance': 0.7, 'location_preference': 'Rural', 'diversity_factor': 0.6, 'company_name': 'Charlie'}

    ]

    prioritized_applications = prioritize_applications(job_applications, user_skills)
    final_result, missed_applications = schedule_applications(prioritized_applications)
    print('Final schedule:',final_result)
    print('-------------------------')
    print('missed_applications:', missed_applications)

    plot_pie_chart(final_result)

from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np

import matplotlib.dates as mdates

# Sample data
# dates = ['2023-11-15', '2023-12-06', '2023-11-06']
# names = [1, 3]

dates = []
names = []
threshold = 2

for app in final_result:
    job_id = app['job_id']
    suggested_date = app['suggested_date']
    date_string = suggested_date.strftime('%Y-%m-%d')
    dates.append(date_string)
    names.append('job_id:'+ str(app['job_id']))

# Convert date strings to datetime
dates = [datetime.strptime(d, "%Y-%m-%d") for d in dates]

# Choose some nice levels
levels = np.tile([1, 2, 3, 4],
                 int(np.ceil(len(dates) / 4)))[:len(dates)]

# Create figure and plot a stem plot with the date
fig, ax = plt.subplots(figsize=(8.8, 4), constrained_layout=True)
ax.set(title="Job Scheduling Dates")

ax.vlines(dates, 0, levels, color="tab:red")  # The vertical stems.
ax.plot(dates, np.zeros_like(dates), "-o",
        color="k", markerfacecolor="w")  # Baseline and markers on it.

# Annotate lines
for d, l, r in zip(dates, levels, names):
    ax.annotate(r, xy=(d, l),
                xytext=(-3, np.sign(l) * 3), textcoords="offset points",
                horizontalalignment="right",
                verticalalignment="bottom" if l > 0 else "top")

# Format x-axis with all dates
ax.xaxis.set_major_locator(mdates.DayLocator())  # Set locator to show every day
ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b %Y"))
plt.setp(ax.get_xticklabels(), rotation=30, ha="right")

# Remove y-axis and spines
ax.yaxis.set_visible(False)
ax.spines[["left", "top", "right"]].set_visible(False)

ax.margins(y=0.1)
plt.show()
