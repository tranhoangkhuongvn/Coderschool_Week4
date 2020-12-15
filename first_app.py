import streamlit as st

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import colors as mcolors

st.title('UFC Summary')
st.write('Here is our data:')



@st.cache(allow_output_mutation=True)
def load_clean_data():
	data = pd.read_csv('./UFC_clean.csv')
	return data


df_clean = load_clean_data()
st.write(df_clean.head(10))

fig = plt.figure(constrained_layout=False, figsize=(20, 15))
fig.suptitle('SOME INSIGHTS FROM LAST WEEK')
gs = fig.add_gridspec(nrows=2, ncols=2, wspace=0.3, hspace=0.3)

ax1 = fig.add_subplot(gs[0,0])
ax2 = fig.add_subplot(gs[0,1])

matchs = df_clean.groupby(['fight_year','weight_class']).count()['Winner'].reset_index()
# matchs = matchs[matchs['weight_class'].isin(['Lightweight','Welterweight','Middleweight','Featherweight','Light Heavyweight'])]
palette = sns.color_palette(n_colors=14)
sns.lineplot(data=matchs, y="Winner", x="fight_year", hue="weight_class", ax = ax1)
ax1.set(title = 'Matchs over the years by the weight class' , xlabel = 'year')
ax1.axvline(x = 2006)

df_clean[df_clean['fight_year'] >= 2006].groupby('weight_class').count()['Winner'].sort_values().plot(kind = 'barh', ax =ax2)
ax2.set(title = 'Number of fights by the weight class' , xlabel = 'no', ylabel = 'weight_class')
st.pyplot(fig)



st.write("""
#### Fight weight class: 
- Weight class : 'Lightweight','Welterweight','Middleweight','Featherweight','Light Heavyweight' 
- Data from 2006 - T6/2019 
- Championship Fights At 3 Rounds: '3 Rnd (5-5-5)' 
""")

weight_select = ['Lightweight','Welterweight','Middleweight','Featherweight','Light Heavyweight']
df = df_clean[df_clean['fight_year']>= 2006]
df = df_clean[df_clean['weight_class'].isin(weight_select)]
df = df[df['Format'].isin(['3 Rnd (5-5-5)'])]

df.describe()


R_fighter = df[['R_fighter','fight_year','Winner','R_SIG_STR_pct','R_TD_pct','R_SIG_STR._landed','R_TOTAL_STR._landed', 'R_TOTAL_STR._att','R_DISTANCE_landed','R_CLINCH_landed','R_GROUND_landed','R_GROUND_att',
               'R_HEAD_landed','R_BODY_landed','R_LEG_landed','total_time_fought(minutes)','last_round']]
B_fighter = df[['B_fighter','fight_year','Winner','B_SIG_STR_pct','B_TD_pct','B_SIG_STR._landed','B_TOTAL_STR._landed','B_TOTAL_STR._att','B_DISTANCE_landed','B_CLINCH_landed','B_GROUND_landed', 'B_GROUND_att',
               'B_HEAD_landed','B_BODY_landed','B_LEG_landed','total_time_fought(minutes)','last_round']]

R_fighter.columns = ['fighter','fight_year','Winner','SIG_STR_pct','TD_pct','SIG_STR._landed','TOTAL_STR._landed','TOTAL_STR._att','DISTANCE_landed','CLINCH_landed','GROUND_landed','GROUND_att',
               'HEAD_landed','BODY_landed','LEG_landed','total_time_min','last_round']

B_fighter.columns = ['fighter','fight_year','Winner','SIG_STR_pct','TD_pct','SIG_STR._landed','TOTAL_STR._landed','TOTAL_STR._att','DISTANCE_landed','CLINCH_landed','GROUND_landed','GROUND_att',
               'HEAD_landed','BODY_landed','LEG_landed','total_time_min','last_round']


RB_fighter = R_fighter.append(B_fighter)  
RB_fighter['Winner_T'] = RB_fighter['Winner'] == RB_fighter['fighter']
RB_fighter['Winner_label'] = np.where(RB_fighter['Winner'] == RB_fighter['fighter'],'Winner','Loser')  
RB_fighter['TOTAL_STR_pct']= np.where(RB_fighter['TOTAL_STR._att'] == 0, 0, RB_fighter['TOTAL_STR._landed']/RB_fighter['TOTAL_STR._att'])
RB_fighter.describe()



st.write("""
#### Question 1: Best timing to get advantages

""")
df1 = df_clean.groupby('last_round', as_index=False).count()[['last_round','No_of_rounds']]
df2 = df_clean.groupby('last_round', as_index=False).sum()['win_by_KO']
df3 = df_clean.groupby('last_round', as_index=False).sum()['win_by_Submission']
finish = pd.concat([df1, df2, df3], axis=1, sort=False)
finish['Chance_to_finish'] = finish['No_of_rounds']/finish['No_of_rounds'].sum()
finish['Chance_to_KO_TKO'] = finish['win_by_KO']/finish['No_of_rounds'].sum()
finish['Chance_to_Submission'] = finish['win_by_Submission']/finish['No_of_rounds'].sum()
Chance_to_finish = finish['Chance_to_finish'].to_list()
Chance_to_KO_TKO = finish['Chance_to_KO_TKO'].to_list()
Chance_to_Submission = finish['Chance_to_Submission'].to_list()
last_round = np.array(finish['last_round'].to_list())
fig, ax = plt.subplots(figsize=(12,5))
bar_width = 0.25

ax.bar(last_round + 0.00, Chance_to_finish , width=bar_width, label = 'Chance_to_finish' , color = 'xkcd:slate blue')
ax.bar(last_round + 0.25, Chance_to_KO_TKO,  width=bar_width,label = 'Chance_to_KO_TKO', color ='xkcd:moss' )
ax.bar(last_round + 0.5, Chance_to_Submission,  width=bar_width, label = 'Chance_to_Submission', color ='xkcd:ochre' )

ax.set(title='Chances of finish per round',
       ylabel= 'Probability',
       xlabel='Round'
      )
plt.xticks(label =last_round , rotation=60)
ax.grid(False)
ax.legend(loc='upper left')
st.pyplot(fig)



fig = plt.figure(constrained_layout=False, figsize=(20, 5))
fig.suptitle('BOUT DURATION AND PERFROMANCE INDICATORS')
gs = fig.add_gridspec(nrows=1, ncols=3,top = 0.8, wspace=0.3, hspace=0.3)

ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])
ax3 = fig.add_subplot(gs[0, 2])

sns.scatterplot(data=RB_fighter, y="TOTAL_STR_pct", x="total_time_min", hue="Winner_label", hue_order = ['Loser','Winner'], ax = ax1 )
ax1.set(title = 'Total strike accuracy' , xlabel = 'Time_bout_min' , ylabel = 'Total strike accuracy %' , xticks = [0,5,10,15])
ax1.axhline(y = 0.6)

sns.scatterplot(data=RB_fighter, y="SIG_STR_pct", x="total_time_min", hue="Winner_label", hue_order = ['Loser','Winner'],ax = ax2)
ax2.set(title = 'Significant strike accuracy' , xlabel = 'Time_bout_min' , ylabel = 'Significant strike accuracy %', xticks = [0,5,10,15])
ax2.axhline(y = 0.5)

sns.scatterplot(data=RB_fighter, y="TD_pct", x="total_time_min", hue="Winner_label", ax = ax3, hue_order = ['Loser','Winner'])
ax3.set(title = 'Takedown accuracy', xlabel = 'Time_bout_min' , ylabel = 'Takedown accuracy %' , xticks = [0,5,10,15])
#plt.show()
st.pyplot(fig)


st.write("""
Total Strike Accuracy, Signiﬁcant Strike Accuracy is reduced over time, and the diﬀerence between winners and losers in this performance indicator becomes less distinct (represented by a reduction in accuracy by winners,and an increase by losers). The best time to take advantage is in the first round, when the strike accuracy is still high.

On the contrary, Takedowns maintaining their frequency. This can be understand that grappling strategy from the position on the ground is prioritized over strikes during the ﬁnal minutes of a bout.

""")


st.write("""
#### Question 2: Significant Strike pace and accuracy
""")

fig = plt.figure(constrained_layout=False, figsize=(20, 8))
fig.suptitle('SIGNIFICANT STRIKE PACE AND ACCURACY')
gs = fig.add_gridspec(nrows=1, ncols= 2,top = 0.9, wspace=0.3, hspace=0.3)

ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])

RB_fighter['SIG_STR_pct_label'] = pd.cut(RB_fighter["SIG_STR_pct"], bins = 20, labels = range(0,100,5))

pd.pivot_table(RB_fighter[['SIG_STR_pct_label','Winner_T', 'Winner_label']], index='SIG_STR_pct_label',columns='Winner_label',values='Winner_T',aggfunc=len).plot(kind= 'bar', ax = ax1)
ax1.set(title = 'Significant strike & win probability', xlabel = 'Significant accuracy%' , ylabel = 'no_of_fighters')

ax1 = ax1.twinx()
RB_fighter.groupby('SIG_STR_pct_label').mean()['Winner_T'].reset_index().plot( ax= ax1, grid = True, ylim = (0,1))
ax1.grid(False)
ax1.set(xlabel = 'Significant accuracy%' , ylabel = 'win probability')

RB_fighter['SIG_STR_per_min'] = RB_fighter['SIG_STR._landed']/RB_fighter['total_time_min']
RB_fighter['SIG_STR_per_min_label'] = RB_fighter['SIG_STR_per_min'].apply(lambda x: '02' if x <= 2 else ('04' if x <= 4 else('06' if x <= 6 else ('08' if x<= 8 else ('10' if x <= 10 else ('12' if x <= 12 else ('14' if x <= 14 else '> 14' )) )))))

pd.pivot_table(RB_fighter[['SIG_STR_per_min_label','Winner_T', 'Winner_label']], index='SIG_STR_per_min_label',columns='Winner_label',values='Winner_T',aggfunc=len).plot(kind= 'bar', ax = ax2)
ax2.set(title = 'Significant strike per min & win probability', xlabel = 'Significant strike per min' , ylabel = 'no_of_fighters')

ax2 = ax2.twinx()
RB_fighter.groupby('SIG_STR_per_min_label').mean()['Winner_T'].plot(ax= ax2, ylim = (0,1))
ax2.grid(False)
ax2.set(xlabel = 'Significant strike per min' , ylabel = 'win probability')

st.pyplot(fig)


st.write("""
#### Significant strike obiviously bring high efficiency in a fight. Maintaining an accuracy rate above 40%, the chances of winning are higher. Looking deeply at the strike frequency, every minute you hit your opponent ~ 5 strikes, the win can be very close

""")

st.write("""
#### Question 3: Positions to take advantage of

""")
st.write("""1. Clinch fighting""")
st.image('./images/clinch.jpg', width=400)
st.write("""2. Ground fighting""")
st.image('./images/ground.jpg', width=400)
st.write("""3. Stand fighting""")
st.image('./images/stand.jpg', width=400)


fig = plt.figure(constrained_layout=False, figsize=(20, 15))
fig.suptitle('POSITION TO TAKE ADVANTAGE OF')
gs = fig.add_gridspec(nrows=2, ncols=3, wspace=0.3, hspace=0.3)

ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])
ax3 = fig.add_subplot(gs[0, 2])

ax4 = fig.add_subplot(gs[1, 0])
ax5 = fig.add_subplot(gs[1, 1])
ax6 = fig.add_subplot(gs[1, 2])


# sns.scatterplot(data=RB_fighter, y="GROUND_landed", x="SIG_STR._landed", hue="Winner_T", ax = ax1)
sns.scatterplot(data=RB_fighter, y="GROUND_landed", x="SIG_STR._landed", hue="Winner_label", hue_order = ['Loser','Winner'], ax = ax1 )
ax1.set(title = 'ground' , xlabel = 'Sig strike landed' , ylabel = 'Ground landed', ylim = (0,100) , xlim = (0,200) )
ax1.axhline(y = 15 , xmax= 1)
ax1.axhline(y = 5 , xmin = 0)
ax1.axvline(x = 50)

sns.scatterplot(data=RB_fighter, y="CLINCH_landed", x="SIG_STR._landed", hue="Winner_label", hue_order = ['Loser','Winner'],ax = ax2)
ax2.set(title = 'ground' , xlabel = 'Sig strike landed' , ylabel = 'Clinch landed', ylim = (0,100) , xlim = (0,200) )

ax2.axhline(y = 5 , xmin = 0)
ax2.axvline(x = 60)

sns.scatterplot(data=RB_fighter, y= "DISTANCE_landed" , x= "SIG_STR._landed", hue="Winner_label", ax = ax3, hue_order = ['Loser','Winner'])
ax3.set(title = 'ground' , xlabel = 'Sig strike landed' , ylabel = 'Distance landed', ylim = (0,100) , xlim = (0,200) )


sns.scatterplot(data=RB_fighter, y="GROUND_landed", x="total_time_min", hue="Winner_label", hue_order = ['Loser','Winner'], ax = ax4 )
ax4.set(title = 'ground' , xlabel = 'Time_bout_min' , ylabel = 'Ground landed', ylim = (0,100) , xlim = (0,15) )
ax4.axhline(y = 3 , xmin = 0)
ax4.axvline(x = 6)


sns.scatterplot(data=RB_fighter, y="CLINCH_landed", x="total_time_min", hue="Winner_label", hue_order = ['Loser','Winner'],ax = ax5)
ax5.set(title = 'ground' , xlabel = 'Time_bout_min' , ylabel = 'Clinch landed', ylim = (0,100) , xlim = (0,15) )

sns.scatterplot(data=RB_fighter, y= "DISTANCE_landed" , x= "total_time_min", hue="Winner_label", ax = ax6, hue_order = ['Loser','Winner'])
ax6.set(title = 'ground' , xlabel = 'Time_bout_min' , ylabel = 'Distance landed', ylim = (0,100) , xlim = (0,15) )

st.pyplot(fig)

st.write("""
Most of the time fighters will strike at long distance, and the significant strikes to win is when they strike the opponent down to the ground

The threshold can be observed and selected from the winning results as follows:

- Significant strikes >= 50 & Ground strike >= 5 or Ground strike >= 15
- Ground strike >= 3 within 6 minutes
- Significant strikes >= 60 & Clinch strike >= 5

""")

RB_fighter['Sig_str_ground'] = (RB_fighter['SIG_STR._landed'] >= 50) & (RB_fighter['GROUND_landed'] >= 5) | (RB_fighter['GROUND_landed'] >=15)

RB_fighter['Ground_time'] = (RB_fighter['GROUND_landed'] >= 3) & (RB_fighter['total_time_min'] <= 6)
RB_fighter['Sig_str_clinch'] = (RB_fighter['SIG_STR._landed'] >= 60) & (RB_fighter['GROUND_landed'] >= 5)

summary1 = RB_fighter.groupby('Sig_str_ground').mean()['Winner_T'].reset_index()
summary1
summary2 = RB_fighter.groupby('Ground_time').mean()['Winner_T'].reset_index()
summary2
summary3 = RB_fighter.groupby('Sig_str_clinch').mean()['Winner_T'].reset_index()
summary3

st.image('./images/south_paw_orthodox.jpeg')
new_df_clean = df_clean.copy()
df_clean['Winning_stance'] = np.where( new_df_clean['Winner'] == new_df_clean['R_fighter'] , new_df_clean['R_Stance'] , new_df_clean['B_Stance'])
#df_clean.head()
fig = plt.figure(constrained_layout=False, figsize=(20, 15))
new_df_clean.groupby('Winning_stance')['R_fighter'].count().plot(kind='bar', figsize=(15, 10))
#st.pyplot()
st.image('./images/winning_stance.png')

st.write("""
If you wanna win a UFC fight, better choose Orthodox stance
""")

st.write("""
#### Summary
- Speed up the fight right from the first round, finish as soon as possible

- 6 significant strikes per min

- Accuracy of landing should be more than 40%

- Trying to get closer after continuous attacks that knock the opponent to the floor(> = 50 sig strike + >= 5 ground strikes)

- Within the first 6 minutes, it's great when strike or take down the opponents to the floor

- At close distance, the clinch can also be used to keep the rhythm of the game until the end of the match

""")
