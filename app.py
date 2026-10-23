"""Small, retrospective hotel-cancellation dashboard for Assignment 4."""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter, StrMethodFormatter
import streamlit as st

st.set_page_config(page_title='Booking Review', page_icon='🏨', layout='wide')
plt.rcParams.update({'font.size': 11, 'axes.spines.top': False,
                     'axes.spines.right': False, 'axes.axisbelow': True})
BLUE = '#3767a6'

@st.cache_data
def load_data():
    return pd.read_csv(Path(__file__).with_name('hotel_bookings.csv'),
                       parse_dates=['arrival_date'])

df = load_data()
st.title('Booking Review — Hotel cancellations')
st.caption('For a hotel revenue manager deciding which booking channels need a cancellation-policy review.')
st.caption('Data: July 2015–August 2017 arrivals, Kaggle historical snapshot. '
           'Production plan: refresh nightly; manager reviews weekly after outcomes settle.')
st.info('Historical completed booking outcomes, not current reservations or a forecast. '
        'Cancelled booked room-nights describe reservation volume; they are not lost revenue or unsold rooms.')

hotel = st.sidebar.selectbox('Hotel', ['All hotels'] + sorted(df['hotel'].unique().tolist()))
months = sorted(df['arrival_date'].dt.strftime('%Y-%m').unique().tolist())
first_month, last_month = st.sidebar.select_slider(
    'Arrival months', options=months, value=(months[0], months[-1]))
all_segments = sorted(df['market_segment'].unique().tolist())
segments = st.sidebar.multiselect('Booking channels (market segment)',
                                  all_segments, default=all_segments)

selected = df[
    df['arrival_date'].dt.strftime('%Y-%m').between(first_month, last_month)
    & df['market_segment'].isin(segments)
].copy()
if hotel != 'All hotels':
    selected = selected[selected['hotel'].eq(hotel)].copy()
if selected.empty:
    st.warning('No bookings match these filters. Select at least one channel or widen the period.')
    st.stop()

selected['booked_nights'] = selected['stays_in_weekend_nights'] + selected['stays_in_week_nights']
selected['cancelled_nights'] = selected['booked_nights'] * selected['is_canceled']
cancelled = int(selected['is_canceled'].sum())
columns = st.columns(3)
columns[0].metric('Bookings in selected cohort', f'{len(selected):,}')
columns[1].metric('Cancelled bookings', f'{cancelled/len(selected):.1%}')
columns[2].metric('Cancelled booked room-nights', f'{selected["cancelled_nights"].sum():,.0f}')
st.caption(f'{cancelled:,} cancellations / {len(selected):,} bookings. '
           'A row is one reservation; repeated-looking reservations are retained because no booking ID is supplied.')

st.subheader('Cancellation rate by arrival month')
monthly = selected.groupby(selected['arrival_date'].dt.to_period('M')).agg(
    bookings=('is_canceled', 'size'), cancelled=('is_canceled', 'sum'))
all_months = pd.period_range(first_month, last_month, freq='M')
monthly = monthly.reindex(all_months)
monthly['rate'] = monthly['cancelled'] / monthly['bookings']
fig, ax = plt.subplots(figsize=(11, 3.7))
positions = list(range(len(monthly)))
ax.plot(positions, monthly['rate'], marker='o', color=BLUE, linewidth=2)
last_position = len(monthly)-1
tick_positions = sorted(set([0, last_position] +
                            [i for i in range(0, len(monthly), 3) if last_position-i >= 2]))
ax.set_xticks(tick_positions, [str(monthly.index[i]) for i in tick_positions])
ax.yaxis.set_major_formatter(PercentFormatter(1))
ax.set_ylim(0, 1)
ax.set_ylabel('Cancelled / bookings')
ax.grid(axis='y', alpha=0.2)
fig.tight_layout()
st.pyplot(fig)
plt.close(fig)
missing_months = monthly.index[monthly['bookings'].isna()].astype(str).tolist()
if missing_months:
    st.caption('No selected bookings in: ' + ', '.join(missing_months) + '. Gaps are not zero cancellation rates.')
st.caption('Months are arrival cohorts, not dates when cancellations were made. '
           'July 2015 and August 2017 are dataset boundaries; comparisons are descriptive and may reflect channel mix.')

st.subheader('Cancelled booked room-nights by channel')
channel = selected.groupby('market_segment').agg(
    bookings=('is_canceled', 'size'), cancelled=('is_canceled', 'sum'),
    cancelled_nights=('cancelled_nights', 'sum')).sort_values('cancelled_nights')
fig, ax = plt.subplots(figsize=(11, 3.8))
bars = ax.barh(channel.index, channel['cancelled_nights'], color=BLUE)
ax.set_xlabel('Booked room-nights attached to cancelled reservations')
ax.xaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))
ax.grid(axis='x', alpha=0.2)
largest = max(float(channel['cancelled_nights'].max()), 1)
ax.set_xlim(0, largest*1.52)
for bar, (_, row) in zip(bars, channel.iterrows()):
    rate = row['cancelled']/row['bookings']
    ax.text(bar.get_width()+largest*.02, bar.get_y()+bar.get_height()/2,
            f'{int(row["cancelled_nights"]):,} | {rate:.1%} | n={int(row["bookings"]):,}',
            va='center', fontsize=10)
fig.tight_layout()
st.pyplot(fig)
plt.close(fig)
st.caption('Labels: cancelled booked room-nights | cancellation rate | total channel bookings. '
           'Review large-volume channels first; small channel samples do not support firm conclusions. '
           'Differences do not establish that a channel causes cancellations.')

with st.expander('Definitions, source, and filtered records'):
    st.write('Cancellation rate = cancelled reservations / all selected reservations. '
             'Booked room-nights = weekend nights + week nights. '
             'All 119,390 source reservations are retained; no prices, occupancy, or live inventory are inferred.')
    st.markdown('[Kaggle: Hotel booking demand](https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand) '
                '· Original authors: Nuno Antonio, Ana Almeida, Luis Nunes. CC BY 4.0.')
    st.write('The shipped CSV preserves every row and only the six columns needed for this view. '
             'Download applies the same filters as the metrics and charts.')
    st.download_button('Download selected reservations', selected.to_csv(index=False),
                       file_name='selected_hotel_bookings.csv', mime='text/csv')
