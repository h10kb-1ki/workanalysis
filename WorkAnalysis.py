import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# 時間分析用のデータフレームを準備
file = 'data.xlsm'
pd.options.display.float_format = '{:.1f}'.format
df = pd.read_excel(file, sheet_name='待ち時間', header=0, index_col=0)

df.columns = ['day', '祝日前週', '祝日前日', '祝日後日', '祝日後週','化療研修',
            '08:30', '09:00', '09:30', '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', 
            '13:00', '13:30', '14:00', '14:30', '15:00', '15:30', '16:00', '16:30']

youbi = np.array(df['day'])
day_of_week = []
for i in youbi:
    if i%7 ==2:
        day_of_week.append('Mon')
    elif i%7 ==3:
        day_of_week.append('Tue')
    elif i%7 ==4:
        day_of_week.append('Wed')
    elif i%7 ==5:
        day_of_week.append('Thu')
    elif i%7 ==6:
        day_of_week.append('Fri')
    elif i%7 ==0:
        day_of_week.append('Sat')
df['day'] = day_of_week
df.fillna(0, inplace=True)

yyyymm = []
for j in range(0, len(df.index)):
    yyyymm.append(str(df.index[j].year) + '/' + str(df.index[j].month))
df['yyyymm'] = yyyymm

# 人員分析用のデータフレームを準備
memb = pd.read_excel(file, sheet_name='人員増減', header=0, index_col=0)

memb.columns = ['day', '祝日前週', '祝日前日', '祝日後日', '祝日後週','化療研修',
            '08:30', '09:00', '09:30', '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', 
            '13:00', '13:30', '14:00', '14:30', '15:00', '15:30', '16:00', '16:30']

Youbi = np.array(memb['day'])
Day_of_week = []
for a in Youbi:
    if a%7 ==2:
        Day_of_week.append('Mon')
    elif a%7 ==3:
        Day_of_week.append('Tue')
    elif a%7 ==4:
        Day_of_week.append('Wed')
    elif a%7 ==5:
        Day_of_week.append('Thu')
    elif a%7 ==6:
        Day_of_week.append('Fri')
    elif a%7 ==0:
        Day_of_week.append('Sat')
memb['day'] = Day_of_week
memb.fillna(0, inplace=True)

yymm = []
for b in range(0, len(memb.index)):
    yymm.append(str(memb.index[b].year) + '/' + str(memb.index[b].month))
memb['yyyymm'] = yymm


st.title('業務分析')

# 抽出条件の設定（サイドバー）
st.sidebar.write('抽出条件')
duration = st.sidebar.multiselect('期間', list(df['yyyymm'].unique()), default=list(df['yyyymm'].unique())) # arrayのままでは× listに変換

OrAnd = st.sidebar.radio('以下の項目の検索条件', ['or検索', 'and検索'])
before_w = st.sidebar.radio('祝日前週', ['考慮しない', '含む', '含まない'])
before_d = st.sidebar.radio('祝日前日', ['考慮しない','含む', '含まない'])
after_d = st.sidebar.radio('祝日後日', ['考慮しない','含む', '含まない'])
after_w = st.sidebar.radio('祝日後週', ['考慮しない','含む', '含まない'])
chemo = st.sidebar.radio('化療研修', ['考慮しない','含む', '含まない'])

# 抽出
if before_w == '含む':
    q_before_w = "祝日前週 == 1.0"
elif before_w == '含まない':
    q_before_w = "祝日前週 == 0.0"
else:
    q_before_w = "祝日前週 == 1.0 or 祝日前週 == 0.0"

if before_d == '含む':
    q_before_d = "祝日前日 == 1.0"
elif before_d == '含まない':
    q_before_d = "祝日前日 == 0.0"
else:
    q_before_d = "祝日前日 ==1.0 or 祝日前日 == 0.0"

if after_d == '含む':
    q_after_d = "祝日後日 == 1.0"
elif after_d == '含まない':
    q_after_d = "祝日後日 == 0.0"
else:
    q_after_d = "祝日後日 == 1.0 or 祝日後日 == 0.0"

if after_w == '含む':
    q_after_w = "祝日後週 == 1.0"
elif after_w == '含まない':
    q_after_w = "祝日後週 == 0.0"
else:
    q_after_w = "祝日後週 == 1.0 or 祝日後週 == 0.0"

if chemo == '含む':
    q_chemo = "化療研修 == 1.0"
elif chemo == '含まない':
    q_chemo = "化療研修 == 0.0"
else:
    q_chemo = "化療研修 == 1.0 or 化療研修 == 0.0"

df = df[(df['yyyymm'].isin(duration))]
memb = memb[(memb['yyyymm'].isin(duration))]

if OrAnd == 'or検索':
    df = df.query(q_before_w + ' or ' + q_before_d + ' or ' + q_after_d + ' or ' + q_after_w + ' or ' + q_chemo)
    memb = memb.query(q_before_w + ' or ' + q_before_d + ' or ' + q_after_d + ' or ' + q_after_w + ' or ' + q_chemo)
elif OrAnd == 'and検索':
    df = df.query(q_before_w)
    df = df.query(q_before_d)
    df = df.query(q_after_d)
    df = df.query(q_after_w)
    df = df.query(q_chemo)

    memb = memb.query(q_before_w)
    memb = memb.query(q_before_d)
    memb = memb.query(q_after_d)
    memb = memb.query(q_after_w)
    memb = memb.query(q_chemo)


if st.sidebar.button('決定'):
    """
    ## 待ち時間
    """
    hit = len(df)
    st.write(f'該当日数 {hit}日')

    df1 = pd.pivot_table(data=df, index='day', aggfunc=np.mean)
    df1 = df1.drop(['祝日前日', '祝日前週', '祝日後日', '祝日後週', '化療研修'], axis=1)
    
    order = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
    df1 = df1.reindex(labels=order).T
    #st.dataframe(df1)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 12))
    plt.rcParams["font.size"] = 18
    plt.subplots_adjust(wspace=0.3, hspace=0.6)

    sns.heatmap(df1, annot=True, fmt='.1f', cmap='Reds', vmax=50, vmin=0, ax=ax1)
    ax1.set_title('Average')


    df2 = pd.pivot_table(data=df, index='day', aggfunc=np.std)
    df2 = df2.drop(['祝日前日', '祝日前週', '祝日後日', '祝日後週', '化療研修'], axis=1)
    df2 = df2.reindex(labels=order).T
    sns.heatmap(df2, annot=True, fmt='.1f', cmap='Greens', vmax=15, vmin=0, ax=ax2)
    ax2.set_title('Stdev')
    st.pyplot(fig)

    """
    ## 人員の増減
    """
    memb1 = pd.pivot_table(data=memb, index='day', aggfunc=np.mean)
    memb1 = memb1.drop(['祝日前日', '祝日前週', '祝日後日', '祝日後週', '化療研修'], axis=1)
    
    order = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
    memb1 = memb1.reindex(labels=order).T
    #st.dataframe(memb1)

    fig2, (ax3, ax4) = plt.subplots(1, 2, figsize=(15, 12))
    plt.rcParams["font.size"] = 18
    plt.subplots_adjust(wspace=0.3, hspace=0.6)

    sns.heatmap(memb1, annot=True, fmt='.1f', cmap='RdBu_r', vmax=5, vmin=-5, ax=ax3)
    ax3.set_title('Average')


    memb2 = pd.pivot_table(data=memb, index='day', aggfunc=np.std)
    memb2 = memb2.drop(['祝日前日', '祝日前週', '祝日後日', '祝日後週', '化療研修'], axis=1)
    memb2 = memb2.reindex(labels=order).T
    sns.heatmap(memb2, annot=True, fmt='.1f', cmap='Greens', vmax=3, vmin=0, ax=ax4)
    ax4.set_title('Stdev')
    st.pyplot(fig2)
