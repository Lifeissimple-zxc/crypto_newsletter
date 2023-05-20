from utils.dependencies import get_gsheet, save_fig, email_with_attachment, DOC_URL
import pandas as pd
from plotly import graph_objects as go
from datetime import datetime
from plotly.subplots import make_subplots
import plotly.express as px
from plotly.colors import n_colors
import numpy as np
import os
import re

#Code Block 1: read data from the document in Gdrive
spreadsheet = get_gsheet(DOC_URL)
sheet = spreadsheet.worksheet('performance')
df_p = pd.DataFrame(sheet.get_all_records())
df_p_bot = df_p[['Asset', 'Total Spent, EUR', 'Asset value, now', 'Gains', 'Return', 'Total Fees, EUR', 'Total Net Spent, EUR']]
df_p_bot = df_p_bot.sort_values(by = 'Total Spent, EUR', ascending = False).reset_index()
df_p_bot['Gain_col'] = ['lightseagreen' if row > 0 else 'crimson' for row in df_p_bot['Gains']]
df_p_bot['return_text'] = ['<b>' + str(round(row * 100, 2)) + '%</b>' for row in df_p_bot['Return']]
print("Prepared Data")

#Code Block 2: create the first visual
fig1 = go.Figure() #create fig
print("Created figure object")
#Add traces block
fig1.add_trace(go.Bar(
    x = df_p_bot['Asset'],
    y = df_p_bot['Total Spent, EUR'],
    name = 'Total invested',
    text = df_p_bot['Total Spent, EUR'],
    textfont = {'size': 25},
    textposition = 'outside',
    marker_color = 'royalblue',
    textfont_color = "royalblue"))
fig1.add_trace(go.Bar(
    x = df_p_bot['Asset'],
    y = df_p_bot['Gains'],
    name = 'Gains',
    text = df_p_bot['Gains'],
    textfont = {'size': 25},
    textposition = 'outside',
    marker_color = df_p_bot['Gain_col'],
    textfont_color = df_p_bot['Gain_col']))
fig1.add_trace(go.Scatter(
    x = df_p_bot['Asset'],
    y = df_p_bot['Return'],
    name = 'Return',
    mode = 'lines+markers+text',
    marker = {'size': 15},
    line = {'color': 'darkviolet'},
    text = df_p_bot['return_text'],
    textposition = 'top right',
    textfont = {'size': 25,'color': "darkviolet"},
    yaxis = 'y2'))
print("Added traces to figure")

#Update figure layout
fig1.update_layout(
    bargroupgap = 0.15,
    plot_bgcolor = 'white',
    yaxis2 = {
       'title': 'Profit % from Total Amount Invested',
       'anchor': 'x',
       'overlaying': 'y',
       'side': 'right'
    },
    yaxis = {
        'title': 'Absolute Amount in EUR',
        'side': 'left'
    },
    legend = {
        'y': 0.99,
        'x': 1.1,
        'xanchor': 'left',
        'font': {
            'size': 20
        }
    },
    title = {
        'text': "<b>Total Spend, Gains & Return</b>",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    }
)
#Update Axes
fig1.update_yaxes(title_font = {'size': 18}, tickfont = {'size': 20})
fig1.update_xaxes(tickfont = {'size': 30})
print("Updated figure layout")

#Save Figure 1 as file
save_fig(fig1, 'Spend_Gain_Return.png', 'png', 1920, 1080, 1)
print("Prepared PNG figure 1")

#Code Block 2: create the second visual
df_stack = df_p_bot[['Asset','Total Spent, EUR', 'Total Net Spent, EUR', 'Gains', 'Total Fees, EUR', 'Asset value, now']]
val_list =[df_stack[v].values for i, v in  enumerate(df_stack.columns)] #prepare list of values for table
table = go.Figure()
table.add_trace(go.Table(
    header = {
        'values' : df_stack.columns
    },
    cells = {
        'values' : val_list
    }
    ))
save_fig(table, 'Asset_Summary.png', 'png', 800, 650, 1)
print("Prepared PNG figure 3")

#Code Block 3: create and send the message
contents = f'''
Total earnings is {(df_p_bot['Gains'].sum())},
Total value of all assets is {(df_p_bot['Asset value, now'].sum())},
Total fees spent is {(df_p_bot['Total Fees, EUR'].sum())}.

Details on the performance are attached.
'''
all_files = os.listdir()
attachments = [file for file in all_files if re.search('png', file)]
email_with_attachment('mararkarp@gmail.com', 'whatever', 'Daily Asset Hermes Message', contents, attachments)
#remove pics
[
    os.remove(file) for file in all_files
    if (re.search('.png', file) and file != "Data visualisation email example.png")
]
print("Sent Email and removed png")

#Code Block 4: Log the data from the day to a Google SpreadSheet
sheet2 = spreadsheet.worksheet('asset_value_history') #Open the needed list
test_df = pd.DataFrame(sheet2.get_all_records())
last_free_row = len(test_df) + 2
update = {}
for col in test_df.columns:
    if col == 'Total': continue
    try:
        update[col] = df_p_bot[df_p_bot['Asset'] == col]['Asset value, now'].values[0]
    except:
        update[col] = str(datetime.now())
update_row = list(update.values())
sheet2.append_row(update_row)
print("Appended snapshot data to the sheet")
