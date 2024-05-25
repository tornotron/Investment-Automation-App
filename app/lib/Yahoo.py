import yfinance as yf
import alpha_vantage as av
import pandas as pd
import numpy as np
import regex as re

pd.set_option("display.max_rows", None)

# Define the number of years and PE ratios to consider

PREV_YEARS_TO_CONSIDER_FCF = [0]  # put atleast [0] or maximum [0,-1,-2] years
PREV_YEARS_TO_CONSIDER_OCF = [0]  # put atleast [0] or maximum [0,-1,-2] years
PREV_YEARS_TO_CONSIDER_ROCE = [0]  # put atleast [0] or maximum [0,-1,-2] years
PREV_YEARS_TO_CONSIDER_ROE = [0]  # put atleast [0] or maximum [0,-1,-2] years
PREV_YEARS_TO_CONSIDER_D2E = [0]  # put atleast [0] or maximum [0,-1,-2] years
PREV_YEARS_TO_CONSIDER_CR = [0]  # put atleast [0] or maximum [0,-1,-2] years
PREV_YEARS_TO_CONSIDER_PS = [0]  # put atleast [0] or maximum [0,-1,-2] years
PREV_YEARS_TO_CONSIDER_SG_1YR = [0]  # put atleast [0] or maximum [0,-1,-2] years
PREV_YEARS_TO_CONSIDER_SG_3YR = [0]  # put atleast [0] or maximum [0,-1,-2] years
PREV_YEARS_TO_CONSIDER_PG_1YR = [0]  # put atleast [0] or maximum [0,-1,-2] years
PREV_YEARS_TO_CONSIDER_PG_3YR = [0]  # put atleast [0] or maximum [0,-1,-2] years
PREV_YEARS_TO_CONSIDER_FV = [0]  # put atleast [0] or maximum [0,-1,-2] years
INDUSTRY_PE = 20
INDEX_PE = 20
USE_INDEX_PE = False
PREV_QUARTERS_TO_CONSIDER_FOR_POSITIVE_SG = [
    0
]  # put atleast [0] or maximum [0,-1,-2] quarters
PREV_QUARTERS_TO_CONSIDER_FOR_POSITIVE_PG = [
    0
]  # put atleast [0] or maximum [0,-1,-2] quarters
PREV_QUARTERS_TO_CONSIDER_FOR_POSITIVE_OP_PG = [
    0
]  # put atleast [0] or maximum [0,-1,-2] quarters


class Yahoo:
    def __init__(self, ticker):
        self.ticker = ticker
        self.company = yf.Ticker(ticker)
        self.info = self.company.info
        self.balance_sheet = self.company.balance_sheet
        self.cashflow = self.company.cashflow
        self.income_stmt = self.company.income_stmt
        self.history_metadata = self.company.history_metadata
        self.financials = self.company.financials
        self.quarterly_financials = self.company.quarterly_financials
        self.history = self.company.history(period="max")
        self.dividends = self.company.dividends
        self.splits = self.company.splits
        self.actions = self.company.actions
        self.major_holders = self.company.major_holders
        self.institutional_holders = self.company.institutional_holders
        self.balance_sheet = self.company.balance_sheet

        self.list_of_info_keys = self.info.keys()
        self.list_of_balance_sheet_keys = self.balance_sheet.index.tolist()
        self.list_of_cashflow_keys = self.cashflow.index.tolist()
        self.list_of_income_stmt_keys = self.income_stmt.index.tolist()
        self.list_of_history_metadata_keys = self.history_metadata.keys()
        self.list_of_financials = self.financials.T.keys()

    def _print_refined_list_of_keys(self, list_of_keys, expression):
        refind_list_of_keys = [
            x for x in list_of_keys if re.search(expression, x, re.IGNORECASE)
        ]
        for key in refind_list_of_keys:
            print("-", key)

    def get_list_of_available_keys(self, expression):
        print("\nInfo Keys:\n")
        self._print_refined_list_of_keys(self.list_of_info_keys, expression)
        print("\nBalance Sheet Keys:\n")
        self._print_refined_list_of_keys(self.list_of_balance_sheet_keys, expression)
        print("\nCashflow Keys:\n")
        self._print_refined_list_of_keys(self.list_of_cashflow_keys, expression)
        print("\nIncome Statement Keys:\n")
        self._print_refined_list_of_keys(self.list_of_income_stmt_keys, expression)
        print("\nHistory Metadata Keys:\n")
        self._print_refined_list_of_keys(self.list_of_history_metadata_keys, expression)
        print("\nFinancials Keys:\n")
        self._print_refined_list_of_keys(self.list_of_financials, expression)

    def calculate_free_cash_flow(self, year):
        free_cash_flow = self.cashflow.loc["Free Cash Flow"]
        return free_cash_flow.iloc[0 - year]

    def _is_free_cash_flow_positive(self):
        for year in PREV_YEARS_TO_CONSIDER_FCF:
            if self.calculate_free_cash_flow(year) < 0:
                return False
        return True

    def calculate_operating_cash_flow(self, year):
        operating_cash_flow = self.cashflow.loc["Operating Cash Flow"]
        return operating_cash_flow.iloc[0 - year]

    def _is_operating_cash_flow_positive(self):
        for year in PREV_YEARS_TO_CONSIDER_OCF:
            if self.calculate_operating_cash_flow(year) < 0:
                return False
        return True

    def calculate_roce(self, year):
        financials = self.financials
        balance_sheet = self.balance_sheet

        # Calculate EBIT (Earnings Before Interest and Taxes)
        ebit = financials.loc["EBIT"]

        # Calculate Capital Employed (Total Assets - Current Liabilities)
        total_assets = balance_sheet.loc["Total Assets"]
        current_liabilities = balance_sheet.loc[
            "Current Liabilities"
        ] 
        capital_employed = total_assets - current_liabilities

        # Calculate ROCE
        roce = ebit / capital_employed
        return roce.iloc[0 - year]

    # Check if ROCE is greater than or equal to 15%

    def _is_roce_greater_than_or_equal_to_15(self):
        for year in PREV_YEARS_TO_CONSIDER_ROCE:
            if self.calculate_roce(year) < 0.15:
                return False
        return True

    def calculate_roe(self, year):
        net_income = self.income_stmt.loc["Net Income"]
        shareholders_equity = self.balance_sheet.loc[
            "Stockholders Equity"
        ] 
        roe = net_income / shareholders_equity
        return roe.iloc[0 - year]

    # Check if ROE is greater than or equal to 15%

    def _is_roe_greater_than_or_equal_to_15(self):
        for year in PREV_YEARS_TO_CONSIDER_ROE:
            if self.calculate_roe(year) < 0.15:
                return False
        return True

    # Check if ROE is greater than or equal to 20%

    def _is_roe_greater_than_or_equal_to_20(self):
        for year in PREV_YEARS_TO_CONSIDER_ROE:
            if self.calculate_roe(year) < 0.2:
                return False
        return True

    # Check if PE is less than industry PE

    def calculate_trailing_pe(self):
        # Fetch the company's data
        info = self.info

        # Get the current market price
        current_price = info.get("currentPrice")

        # Get the trailing twelve months earnings per share
        eps_ttm = info.get("trailingEps")

        # Check if the necessary information is available
        if current_price is not None and eps_ttm is not None and eps_ttm != 0:
            # Calculate the trailing P/E ratio
            trailing_pe = current_price / eps_ttm
            return trailing_pe
        else:
            return "Required data to calculate trailing P/E is not available."

    def _is_pe_less_than_benchmark_pe(self, useindex=USE_INDEX_PE):
        # Calculate the trailing P/E ratio
        trailing_pe = self.calculate_trailing_pe()
        if useindex:
            industry_pe = INDEX_PE
        else:
            industry_pe = INDUSTRY_PE

        if trailing_pe < industry_pe:
            return True
        else:
            return False

    def calculate_debt_to_equity_ratio(self, year):
        balance_sheet = self.balance_sheet
        total_liabilities = balance_sheet.loc[ "Long Term Debt" ] + balance_sheet.loc["Current Debt"]
        total_equity = balance_sheet.loc[
            "Stockholders Equity"
        ] 
        debt_to_equity_ratio = total_liabilities / total_equity
        return debt_to_equity_ratio.iloc[0 - year]

    # Check if the company has a debt to equity ratio of less than 2

    def _is_debt_to_equity_ratio_less_than_2(self):
        for year in PREV_YEARS_TO_CONSIDER_D2E:
            if self.calculate_debt_to_equity_ratio(year) >= 2:
                return False
        return True

    # Check if the company has a debt to equity ratio of less than 0.3

    def _is_debt_to_equity_ratio_less_than_0_dot_3(self):
        for year in PREV_YEARS_TO_CONSIDER_D2E:
            if self.calculate_debt_to_equity_ratio(year) >= 0.3:
                return False
        return True

    # Check if the company has a debt to equity ratio of less than or equal to 0.2
    def _is_debt_to_equity_ratio_less_than_or_equal_to_0_dot_2(self):
        for year in PREV_YEARS_TO_CONSIDER_D2E:
            if self.calculate_debt_to_equity_ratio(year) > 0.2:
                return False
        return True

    def calculate_current_ratio(self, year):
        balance_sheet = self.balance_sheet
        total_current_assets = balance_sheet.loc[
            "Current Assets"
        ]  
        total_current_liabilities = balance_sheet.loc[
            "Current Liabilities"
        ] 
        current_ratio = total_current_assets / total_current_liabilities
        return current_ratio.iloc[0 - year]

    # Check if the company has a current ratio of greater than 2

    def _is_current_ratio_greater_than_2(self):
        for year in PREV_YEARS_TO_CONSIDER_CR:
            if self.calculate_current_ratio(year) <= 2:
                return False
        return True

    def calculate_piotroski_f_score(self, year):
        financials = self.financials.T  # Transpose for easier row access
        balance_sheet = self.balance_sheet.T  # Transpose
        cash_flow = self.cashflow.T  # Transpose

        n = 0 - year

        # Initialize Piotroski score
        f_score = 0

        # Criteria 1: Positive net income
        f_score += 1 if financials["Net Income"].iloc[n] > 0 else 0

        # Criteria 2: Positive return on assets
        f_score += (
            1
            if financials["Net Income"].iloc[n] / balance_sheet["Total Assets"].iloc[n]
            > 0
            else 0
        )

        # Criteria 3: Positive operating cash flow
        f_score += (
            1 if cash_flow["Operating Cash Flow"].iloc[n] > 0 else 0
        ) 

        # Criteria 4: Cash flow from operations greater than net income
        f_score += (
            1
            if cash_flow["Operating Cash Flow"].iloc[n]
            > financials["Net Income"].iloc[n]
            else 0
        )

        # Criteria 5: Lower ratio of long term debt in the current period compared to the previous one
        lt_debt_current = balance_sheet["Long Term Debt"].iloc[n]
        lt_debt_previous = balance_sheet["Long Term Debt"].iloc[n + 1]
        f_score += 1 if lt_debt_current < lt_debt_previous else 0

        # Criteria 6: Higher current ratio this year compared to the previous year
        current_ratio_current = (
            balance_sheet["Current Assets"].iloc[n]
            / balance_sheet["Current Liabilities"].iloc[n]
        ) 
        current_ratio_previous = (
            balance_sheet["Current Assets"].iloc[n + 1]
            / balance_sheet["Current Liabilities"].iloc[n + 1]
        ) 
        f_score += 1 if current_ratio_current > current_ratio_previous else 0

        # Criteria 7: No new shares issued (compare the number of shares outstanding)
        # This criterion may require data not available in standard financial statements

        # Criteria 8: Higher gross margin compared to the previous year
        gross_margin_current = (
            financials["Total Revenue"].iloc[n] - financials["Cost Of Revenue"].iloc[n]
        ) / financials["Total Revenue"].iloc[n]
        gross_margin_previous = (
            financials["Total Revenue"].iloc[n + 1]
            - financials["Cost Of Revenue"].iloc[n + 1]
        ) / financials["Total Revenue"].iloc[n + 1]
        f_score += 1 if gross_margin_current > gross_margin_previous else 0

        # Criteria 9: Higher asset turnover ratio compared to the previous year
        asset_turnover_current = (
            financials["Total Revenue"].iloc[n] / balance_sheet["Total Assets"].iloc[n]
        )
        asset_turnover_previous = (
            financials["Total Revenue"].iloc[n + 1]
            / balance_sheet["Total Assets"].iloc[n + 1]
        )
        f_score += 1 if asset_turnover_current > asset_turnover_previous else 0

        return f_score

    # Check if piotroski f score is greater than 7

    def _is_piotroski_f_score_greater_than_7(self):
        for year in PREV_YEARS_TO_CONSIDER_PS:
            if self.calculate_piotroski_f_score(year) <= 7:
                return False
        return True
    
    def calculate_face_value(self, year):
        FV = self.balance_sheet.loc['Capital Stock']/self.balance_sheet.loc['Share Issued']
        return int(FV.iloc[0-year])

    def calculate_sales_growth_for_1_yr(self, year):
        financials = self.financials.T  # Transpose for easier row access

        n = 0 - year
        # Calculate one year sales growth
        try:
            current_year_sales = financials["Total Revenue"].iloc[n]
            previous_year_sales = financials["Total Revenue"].iloc[n + 1]

            # Calculate sales growth in percentage
            sales_growth = (
                current_year_sales - previous_year_sales
            ) / previous_year_sales
            return sales_growth
        except Exception as e:
            return f"Error calculating sales growth: {str(e)}"

    # Check if slaes growth for 1 year is greater than or equal to 10%

    def _is_1yr_sales_growth_greater_than_or_equal_to_10(self):
        for year in PREV_YEARS_TO_CONSIDER_SG_1YR:
            if self.calculate_sales_growth_for_1_yr(year) < 0.1:
                return False
        return True

    def calculate_sales_growth_for_3_yr(self, year):
        financials = self.financials.T  # Transpose for easier row access

        n = 0 - year
        # Calculate one year sales growth
        try:
            current_year_sales = financials["Total Revenue"].iloc[n]
            third_preious_year_sales = financials["Total Revenue"].iloc[n + 2]

            # Calculate sales growth in percentage
            sales_growth = (
                current_year_sales - third_preious_year_sales
            ) / third_preious_year_sales
            return sales_growth
        except Exception as e:
            return f"Error calculating sales growth: {str(e)}"

    # Check if slaes growth for 3 year is greater than or equal to 10%

    def _is_3yr_sales_growth_greater_than_or_equal_to_10(self):
        for year in PREV_YEARS_TO_CONSIDER_SG_3YR:
            if self.calculate_sales_growth_for_3_yr(year) < 0.1:
                return False
        return True

    def calculate_profit_growth_for_1_yr(self, year):
        financials = self.financials.T  # Transpose for easier row access

        n = 0 - year
        # Calculate one year profit growth
        try:
            current_year_profit = financials["Gross Profit"].iloc[n]
            previous_year_profit = financials["Gross Profit"].iloc[n + 1]

            # Calculate profit growth in percentage
            profit_growth = (
                current_year_profit - previous_year_profit
            ) / previous_year_profit
            return profit_growth
        except Exception as e:
            return f"Error calculating profit growth: {str(e)}"

    # Check if profit growth for 1 year is greater than or equal to 10%

    def _is_1yr_profit_growth_greater_than_or_equal_to_10(self):
        for year in PREV_YEARS_TO_CONSIDER_PG_1YR:
            if self.calculate_profit_growth_for_1_yr(year) < 0.1:
                return False
        return True

    def calculate_profit_growth_for_3_yr(self, year):
        financials = self.financials.T  # Transpose for easier row access

        n = 0 - year
        # Calculate one year profit growth
        try:
            current_year_profit = financials["Gross Profit"].iloc[n]
            third_preious_year_profit = financials["Gross Profit"].iloc[n + 2]

            # Calculate profit growth in percentage
            profit_growth = (
                current_year_profit - third_preious_year_profit
            ) / third_preious_year_profit
            return profit_growth
        except Exception as e:
            return f"Error calculating profit growth: {str(e)}"

    # Check if slaes growth for 3 year is greater than or equal to 10%

    def _is_3yr_profit_growth_greater_than_or_equal_to_10(self):
        for year in PREV_YEARS_TO_CONSIDER_PG_3YR:
            if self.calculate_profit_growth_for_3_yr(year) < 0.1:
                return False
        return True

    def calculate_sales_growth_for_1_quarter(self, quarter):
        financials = self.quarterly_financials.T  # Transpose for easier row access

        n = 0 - quarter
        # Calculate one quarter sales growth
        try:
            current_quarter_sales = financials["Total Revenue"].iloc[n]
            previous_quarter_sales = financials["Total Revenue"].iloc[n + 1]

            # Calculate sales growth in percentage
            sales_growth = current_quarter_sales - previous_quarter_sales
            return sales_growth
        except Exception as e:
            return f"Error calculating sales growth: {str(e)}"

    # Check if sales growth for previous quarters is positive

    def _is_QOQ_sales_growth_positive(self):
        for quarter in PREV_QUARTERS_TO_CONSIDER_FOR_POSITIVE_SG:
            if self.calculate_sales_growth_for_1_quarter(quarter) < 0:
                return False
        return True

    def calculate_profit_growth_for_1_quarter(self, year):
        financials = self.quarterly_financials.T  # Transpose for easier row access

        n = 0 - year
        # Calculate one quarter profit growth
        try:
            current_quarter_profit = financials["Gross Profit"].iloc[n]
            previous_quarter_profit = financials["Gross Profit"].iloc[n + 1]

            # Calculate profit growth in percentage
            profit_growth = current_quarter_profit - previous_quarter_profit
            return profit_growth
        except Exception as e:
            return f"Error calculating profit growth: {str(e)}"

    # Check if profit growth for previous quarters is positive

    def _is_QOQ_profit_growth_positive(self):
        for quarter in PREV_QUARTERS_TO_CONSIDER_FOR_POSITIVE_PG:
            if self.calculate_profit_growth_for_1_quarter(quarter) < 0:
                return False
        return True

    def calculate_EBITDA_growth_for_1_quarter(self, year):
        financials = self.quarterly_financials.T  # Transpose for easier row access

        n = 0 - year
        # Calculate one quarter EBITDA growth
        try:
            current_quarter_EBITDA = financials["EBITDA"].iloc[n]
            previous_quarter_EBITDA = financials["EBITDA"].iloc[n + 1]

            # Calculate EBITDA growth in percentage
            EBITDA_growth = current_quarter_EBITDA - previous_quarter_EBITDA
            return EBITDA_growth
        except Exception as e:
            return f"Error calculating EBITDA growth: {str(e)}"

    # Check if operating profit growth for previous quarters is positive

    def _is_QOQ_operating_profit_growth_positive(self):
        for quarter in PREV_QUARTERS_TO_CONSIDER_FOR_POSITIVE_PG:
            if self.calculate_EBITDA_growth_for_1_quarter(quarter) < 0:
                return False
        return True

    def do_prelimenary_checks_and_get_points(self):
        points = 0
        if self._is_roe_greater_than_or_equal_to_15():
            points += 1
        if self._is_roce_greater_than_or_equal_to_15():
            points += 1
        if self._is_debt_to_equity_ratio_less_than_or_equal_to_0_dot_2():
            points += 1
        if self._is_1yr_sales_growth_greater_than_or_equal_to_10():
            points += 1
        if self._is_3yr_sales_growth_greater_than_or_equal_to_10():
            points += 1
        if self._is_1yr_profit_growth_greater_than_or_equal_to_10():
            points += 1
        if self._is_3yr_profit_growth_greater_than_or_equal_to_10():
            points += 1
        if self._is_pe_less_than_benchmark_pe():
            points += 1
        if self._is_QOQ_sales_growth_positive():
            points += 1
        if self._is_QOQ_profit_growth_positive():
            points += 1
        if self._is_QOQ_operating_profit_growth_positive():
            points += 1

        return points

    def do_management_parameters_check_and_get_points(self):
        points = 0

        if self._is_roce_greater_than_or_equal_to_15():
            points += 1
        if self._is_debt_to_equity_ratio_less_than_0_dot_3():
            points += 1
        if self._is_current_ratio_greater_than_2():
            points += 1
        if self._is_piotroski_f_score_greater_than_7():
            points += 1
        return points

    def do_eps_check_and_get_points(self, year):
        points = 0

        FV = self.calculate_face_value(year)
        eps = self.info.get("trailingEps")

        if eps >= 3 * FV:
            points += 3
        elif eps >= 2 * FV:
            points += 2
        elif eps >= FV:
            points += 1

        return points

    def do_pe_multiples_nifty_check_and_get_points(self):
        points = 0

        if self.calculate_trailing_pe() > 20:
            points += 1
        elif self.calculate_trailing_pe() > 15:
            points += 2
        else:
            points += 3

        return points

    def do_roe_check_and_get_points(self, year):
        points = 0

        if self.calculate_roe(year) > 0.22:
            points += 3
        elif self.calculate_roe(year) > 0.18:
            points += 2
        elif self.calculate_roe(year) > 0.15:
            points += 1
        return points

    def do_dividend_yield_check_and_get_points(self):
        points = 0

        if self.info["dividendYield"] > 0.010:
            points += 3
        elif self.info["dividendYield"] > 0.005:
            points += 2
        elif self.info["dividendYield"] > 0.000:
            points += 1
        return points

    def do_roa_check_and_get_points(self, year):
        points = 0

        ROA = self.financials.loc['Net Income'].iloc[0-year]/((self.balance_sheet.loc['Total Assets'].iloc[0-year]+self.balance_sheet.loc['Total Assets'].iloc[1-year])/2)
        if ROA > 0.22:
            points += 3
        elif ROA > 0.16:
            points += 2
        elif ROA > 0.10:
            points += 1
        return points

    def calculate_EVEBITDA(self):
        financials = self.financials.T  # Transpose for easier row access

        # Calculate EBITDA
        try:
            EBITDA = financials["EBITDA"].iloc[0]
            enterprise_value = self.info.get("enterpriseValue")
            EVEBITDA = enterprise_value / EBITDA
            return EVEBITDA
        except Exception as e:
            return f"Error calculating EVEBITDA: {str(e)}"

    def do_evebitda_check_and_get_points(self):
        points = 0

        if self.calculate_EVEBITDA() < 9:
            points += 3
        elif self.calculate_EVEBITDA() < 12:
            points += 2
        elif self.calculate_EVEBITDA() < 15:
            points += 1

        return points

    def do_index_parameter_scaling_and_get_points(self):
        points = 0

        points += self.do_management_parameters_check_and_get_points()
        points += self.do_eps_check_and_get_points(0)
        points += self.do_pe_multiples_nifty_check_and_get_points()
        points += self.do_roe_check_and_get_points(0)
        points += self.do_dividend_yield_check_and_get_points()
        points += self.do_roa_check_and_get_points(0)
        points += self.do_evebitda_check_and_get_points()
        return points


tickers = ["CHEMFAB.NS"]
# for ticker in tickers:
#     try:
#         print(Yahoo(ticker).do_prelimenary_checks_and_get_points())
#     except Exception as e:
#         print("NULL")
#     print("Done")

company = Yahoo("CHEMFAB.NS")
print(company.do_management_parameters_check_and_get_points())
print(company.do_eps_check_and_get_points(0))
print(company.do_pe_multiples_nifty_check_and_get_points())
print(company.do_roe_check_and_get_points(0))
print(company.do_dividend_yield_check_and_get_points())
print(company.do_roa_check_and_get_points(0))
print(company.do_evebitda_check_and_get_points())
