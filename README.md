# Booking Review — Hotel cancellations

This is a small Streamlit dashboard for a hotel revenue manager. It uses Pandas filtering, sidebar widgets, `st.columns`, `st.metric` and Matplotlib charts following the course Data App Tutorial and Lab. The app is a retrospective prototype, not a live booking system.

## Step 1 — Dataset and decision-maker

**Dataset:** [Hotel booking demand on Kaggle](https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand), version 1, published by Jesse Mostipak. The page credits the original *Hotel booking demand datasets* article by Nuno Antonio, Ana Almeida and Luis Nunes, Data in Brief 22 (2019), and the TidyTuesday preparation by Thomas Mock and Antoine Bichat. License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

These are real historical bookings for one city hotel and one resort hotel. One row is one reservation, with arrivals from July 1, 2015 to August 31, 2017. The original file has 119,390 rows and 32 columns. The committed `hotel_bookings.csv` retains all 119,390 rows but projects only six columns and constructs one arrival-date field from the original year, month and day. It is under 25 MB; no rows were sampled. Run `hotel-eda.ipynb` for the source download, missing-value checks, distributions and projection code.

**One intended user:** the hotel revenue manager, who reviews settled booking outcomes each Monday before discussing channel contracts and cancellation terms with the reservations team. The name “Booking Review” is the proposed project/team label; the submitting student should replace it if their actual team uses another name.

## Step 2 — Why a dashboard

**Decision rule:** If the revenue manager sees that a channel accounts for a large volume of cancelled booked room-nights and a rising cancellation rate, they will review that channel's booking terms and follow-up process with the reservations team before proposing a policy change. A chart does not by itself justify increasing deposits: the manager still needs to check contractual restrictions, demand and potential customer loss.

In the proposed business workflow without this dashboard, the manager would export reservations, repeat spreadsheet calculations and reconcile counts across hotel and channel views each week. That creates repeated preparation and denominator mistakes. This is a workflow assumption for this prototype, not a claim about measured time savings at an actual hotel.

A dashboard earns its place because the same manager returns to the same questions and changes hotel, arrival period and channel scope. A weekly email can summarize totals but cannot answer those follow-up questions interactively. A static report suits an occasional deep review. An alert is useful for a predefined threshold but still needs context before action; it would complement this dashboard rather than replace the comparison views.

## Step 3 — What matters and why

The EDA finds substantial cancellation volume and a channel mix that is useful to compare. The opening view has exactly three headline numbers:

1. **Booking count** establishes the denominator. A high rate in a tiny population should not drive a major decision.
2. **Cancellation rate** is cancelled reservations divided by all selected reservations. It indicates how often booked demand fails to complete.
3. **Cancelled booked room-nights** sums weekend and weekday nights for cancelled reservations. It distinguishes losing a one-night booking from a long reservation. It measures booked reservation volume, not final lost revenue or unsold inventory.

The middle contains two charts. The arrival-month cancellation-rate line shows whether the pattern is changing across cohorts. The channel bar chart shows where cancelled reservation volume is concentrated; labels include the cancellation rate and total booking count, so volume and rate can be read together. All metrics, charts and the optional CSV export use the same filters.

Only three filters are included: hotel, arrival-month range, and booking channel. A manager must isolate the property they own, compare periods and inspect a channel. Additional demographic or numerical sliders would increase effort without directly supporting the stated review. The hotel selector is first in the sidebar because property scope comes before interpreting the numbers.

The order is deliberate: scope controls in the sidebar; headline metrics at the top; the trend, then channel concentration; source definitions and downloadable filtered reservations in a collapsed section. The detail export supports an actual follow-up, while an always-open raw table would push the explanation below the fold.

### Things deliberately excluded

- **A geographic map.** There are only two hotel groups and no useful booking-level coordinates. A map would add visual space without changing which channel the manager reviews.
- **Lead-time and guest-demographic distributions.** The lead-time EDA is useful background, but a histogram does not say which channel warrants action. Demographics add segmentation without a decision rule in this project.
- **Average daily rate and a lost-revenue estimate.** Booked rates are not collected revenue. A cancelled room may be resold, and refunds, fees and occupancy capacity are absent. Multiplying price by cancelled nights would invite an unsupported financial conclusion.

### What could mislead, and how it is handled

- This is a frozen 2015–2017 snapshot. The app says so near the title; it never implies today's bookings are visible.
- Months group **arrival cohorts**, not the date a cancellation happened. Boundary months are flagged and no claims about real-time cancellation timing are made.
- If filtering leaves a month with no bookings, the line has a gap rather than a false zero cancellation rate. Empty selections show an explanatory message.
- The source contains repeated-looking rows and no unique booking ID. I retain all reservations rather than delete potentially valid separate bookings.
- Source fields not used by the dashboard have missing values. The six selected app fields are checked for completeness; unknown/undefined channel labels, when present, remain visible.
- Cancellation rates use their actual selected booking count. Small channel populations are shown in labels and explicitly cautioned against.
- Zero-night bookings remain in the reservation denominator and naturally add zero room-nights. This preserves the source rather than silently changing the population.
- A channel association is not a causal effect. These data alone cannot prove that a new deposit policy will reduce cancellations or increase profit.

## Step 4 — Refresh and review cadence

In a production version I would refresh the reservation-system extract nightly, after the day's outcomes settle. The manager would review it weekly on Monday, when channel and cancellation-policy discussions can lead to action. Continuous refresh adds little value for this weekly decision and would make incomplete cohorts easy to misread.

The production analysis should compare completed arrival cohorts after their stay outcomes are known; it should not label still-active future reservations as successful stays. The metric tracked would be each channel's cancellation rate. I propose a review trigger when its latest completed-week rate rises at least **five percentage points** above its preceding **eight complete weeks**, with at least **100 bookings in both comparison populations**. This is an initial operating proposal, not a statistically calibrated threshold, a tested causal rule, or an implemented automated alert.

A day's delay normally would not change the weekly meeting. A week's delay can hide a newly concentrated channel problem until after another contract or booking-policy discussion. The cost is missed opportunities for investigation, not an amount that this dataset can quantify. Inventory availability would need a separate, faster operational feed and is outside this dashboard.

The included CSV does not refresh automatically. The app displays the historical period and the intended nightly cadence; this document separates that production proposal from the actual frozen demo.

## Run locally

This project was initialized with `uv init --python 3.14` and uses its committed `pyproject.toml`, `.python-version` and `uv.lock`.

```bash
uv sync --locked
uv run streamlit run app.py
```

The app CSV is resolved relative to `app.py`, so the app does not depend on a machine-specific absolute path. An Internet connection is not required to load the included data. The EDA's optional raw-source download does require Internet access; its saved outputs can be read without rerunning it.

## Deploy from the submitting student's accounts

1. Review this README, confirm each design choice and put the explanations in your own words. Replace the proposed team label in `app.py` if necessary.
2. Create a public repository under **your own GitHub account**, containing this folder's files. Do not include `.venv`, caches or credentials.
3. Log into **your own Streamlit Cloud account** and choose that repository, branch `main`, and main file `app.py`.
4. Under **Advanced settings**, select **Python 3.14**, as required by the course and this project.
5. Deploy, open the live app, and exercise the filters. Check that its counts match the local default and filtered views.
6. Paste the actual deployed-app URL and personal GitHub repository URL into the **first Markdown cell of `phone-trade-in.ipynb`**. Do not submit the local-only status text as if it were a live link.

Course references: [group exercise](https://bana409.harrywang.me/docs/lectures/data-app/in-class-group-exercise), [tutorial](https://bana409.harrywang.me/docs/lectures/data-app/data-app-tutorial), [lab](https://bana409.harrywang.me/docs/lectures/data-app/data-app-lab).
