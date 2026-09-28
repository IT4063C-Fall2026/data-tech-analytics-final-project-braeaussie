# Lyn Ausdenmoore IT4063C Final Project
# How have rising tuition costs impacted student loan debt over the years, based on average student/household income?


from import_data import load_tuition, load_loan_debt, load_income

tuition = load_tuition()
loan_debt = load_loan_debt("b1cd19d8927afcba01292e38a5f5f0e3")
income = load_income("b1cd19d8927afcba01292e38a5f5f0e3")

df = tuition.merge(loan_debt, on='Year').merge(income[['Year','Median_Income']], on='Year')

df.to_csv("data/final_dataset.csv", index=False)
