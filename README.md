# Booking Review — Hotel Cancellations

**Live app:** [Open the dashboard](https://hotel-booking-review-hfgzd3sede6bzzizvgteei.streamlit.app/)  
**GitHub repository:** [https://github.com/OuLiyuan033/hotel-booking-review](https://github.com/OuLiyuan033/hotel-booking-review)

## Step 1 — Dataset and decision-maker

**Dataset:** [Hotel booking demand on Kaggle](https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand), version 1. The data cover a city hotel and a resort hotel. They contain 119,390 reservations with arrival dates from July 2015 to August 2017. Each row represents one reservation.

The source credits the original study by Nuno Antonio, Ana Almeida, and Luis Nunes, published in *Data in Brief* in 2019, and the TidyTuesday preparation by Thomas Mock and Antoine Bichat. The dataset is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

The app uses all 119,390 rows. Its CSV keeps the six fields needed for the dashboard: arrival date, hotel, market segment, cancellation status, and weekend and weekday nights. It combines the original year, month, and day columns into one arrival date. The source file has 32 columns; the app does not need the rest.

The dashboard is for a **hotel revenue manager**. The manager reviews it each Monday before discussing booking channels, cancellation terms, and follow-up with the reservations team.

## Step 2 — Why use a dashboard?

The manager asks the same questions each week: how many reservations were made, what share was cancelled, and which channels account for the most cancelled room-nights? If a channel has a high cancellation rate and a large volume of cancelled room-nights, the manager can review that channel's terms and follow-up process before proposing a change.

Without the dashboard, the manager would export reservations and repeat the counts and comparisons in a spreadsheet. This is an assumed workflow for the project; the data do not measure the time or errors it causes.

A dashboard suits a recurring review because the manager can compare hotels, months, and channels in one place. A weekly email would give the totals but not answer follow-up questions. A report is better for a one-time review. An alert can flag a threshold, but the manager still needs the surrounding data to understand it.

## Step 3 — What the dashboard shows

The app starts with three metrics:

- **Bookings:** the number of reservations in the selected filters. This gives context for the other metrics.
- **Cancellation rate:** cancelled reservations divided by all selected reservations.
- **Cancelled booked room-nights:** the weekend and weekday nights attached to cancelled reservations. This measures reservation volume, not lost revenue or unsold rooms.

Two charts support the review. The line chart shows cancellation rate by arrival month. The bar chart shows cancelled booked room-nights by booking channel, with each channel's cancellation rate and booking count alongside it. The manager can filter by hotel, arrival-month range, and market segment. Metrics and charts use the same filters. A filtered reservation download is available under the definitions and source details.

The page puts filters first, then the three metrics, then the trend and channel comparison. Detailed records come last because most users need the summary before the underlying rows.

### What is left out

- **A map:** the data cover two hotel groups and do not include useful booking-level coordinates.
- **Lead-time and guest-demographic charts:** these are useful for exploration, but they do not answer which channel the manager should review.
- **Average daily rate and estimated lost revenue:** a cancelled reservation may be resold. The data do not show refunds, fees, final revenue, or whether a room stayed empty, so a revenue-loss estimate would not be supported.

### Data limits and how the app handles them

- The data are a historical snapshot from 2015–2017. The app shows the date range and does not present the figures as current bookings.
- Months refer to arrival dates, not the dates when cancellations occurred. July 2015 and August 2017 are the dataset boundaries, so comparisons are descriptive and may also reflect changes in channel mix.
- A month with no bookings appears as a gap in the line chart, not as a zero cancellation rate.
- The source has no unique reservation ID and contains repeated-looking rows. The app retains all rows because they may represent separate reservations.
- The selected app fields have no missing values. Small channel groups are labelled with their booking counts and should be interpreted with care.
- Zero-night reservations remain in the booking count and add zero room-nights. Channel differences show association; they do not prove that a channel causes cancellations.

## Step 4 — Refresh and review schedule

In a production system, I would refresh the data nightly after that day's outcomes are available. The revenue manager would review the dashboard each Monday. Real-time updates would add little value for this weekly decision and could make incomplete arrival cohorts harder to interpret.

The metric to monitor is each channel's cancellation rate. I propose a review when the rate for the latest completed week is at least **5 percentage points** above the average for the previous **8 complete weeks**, with at least **100 bookings in each period**. This is an initial proposal, not a threshold tested on this dataset or an alert built into the app.

A one-day delay is unlikely to change the Monday review. A week-long delay could postpone an investigation until after a channel or cancellation-policy discussion. The dataset cannot show the financial cost of that delay. The bundled CSV is static and does not refresh automatically; nightly refresh describes the production plan.

## Run locally

The project uses Python 3.14 and the included `uv.lock` file.

```bash
uv sync --locked
uv run streamlit run app.py
```

The app reads `hotel_bookings.csv` from its own folder and does not need to download data when it starts. In the provided package, the EDA notebook reads the full source file from the `sources` folder beside this app folder. If you publish only this app folder, the notebook downloads the Kaggle dataset when needed.

## Deploy

Publish this project to a public GitHub repository under the submitting student's account. In Streamlit Community Cloud, create an app from that repository, select the `main` branch and `app.py`, then choose Python 3.14 in **Advanced settings**. After deployment, check the filters and confirm that the default view shows 119,390 bookings, a 37.0% cancellation rate, and 154,217 cancelled booked room-nights.
