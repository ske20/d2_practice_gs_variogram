# Applied Geostatistics and Reservoir Data Analysis Quiz

A Streamlit objective-question quiz for students. It contains 20 medium-level questions covering histogram interpretation, descriptive statistics, percentiles, probability, probability density functions, and Monte Carlo simulation using reservoir properties and facies.

## Student experience

- One question is displayed at a time.
- Students select one option and submit it.
- The correct answer is displayed in green.
- An explanation is displayed after submission.
- The running score and progress are updated automatically.
- A full answer review is available after completion.
- No file uploader or question-bank interface is displayed.

## Repository files

```text
streamlit_app.py
questions_file.csv
requirements.txt
README.md
.gitignore
```

## Run locally

1. Install Python 3.10 or later.
2. Open a terminal in the repository folder.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Start the app:

```bash
streamlit run streamlit_app.py
```

## Deploy on Streamlit Community Cloud

1. Create a private GitHub repository.
2. Upload all files from this package to the repository root.
3. In Streamlit Community Cloud, create a new app.
4. Select the private repository and branch.
5. Set the main file path to `streamlit_app.py`.
6. Deploy the app.
7. Configure the app's sharing settings for the intended students.

## Updating questions

Edit `questions_file.csv` while preserving these column names:

```text
subject,question,option_a,option_b,option_c,option_d,correct_answer,explanation
```

Use only `A`, `B`, `C`, or `D` in `correct_answer`. Keep the same subject title in every row. Commit the updated CSV to GitHub; Streamlit will redeploy the revised application.

## Important assessment note

A private repository prevents ordinary viewers from browsing the source files. However, this project is intended for teaching and formative assessment rather than a high-security examination. Do not place passwords, tokens, or other secrets in the CSV or Python source.
