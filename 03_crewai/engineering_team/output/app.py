from accounts import Account
import gradio as gr

account = None

def create_account(username: str, initial_deposit: float):
    global account
    account = Account(username, initial_deposit)
    return f"Account created for {username} with initial deposit of ${initial_deposit:.2f}"

def deposit(amount: float):
    if account is None:
        return "No account found. Please create an account first."
    try:
        account.deposit(amount)
        return f"Deposited ${amount:.2f}. New balance: ${account.balance:.2f}"
    except ValueError as e:
        return str(e)

def withdraw(amount: float):
    if account is None:
        return "No account found. Please create an account first."
    try:
        account.withdraw(amount)
        return f"Withdrew ${amount:.2f}. New balance: ${account.balance:.2f}"
    except ValueError as e:
        return str(e)

def buy_shares(symbol: str, quantity: int):
    if account is None:
        return "No account found. Please create an account first."
    try:
        account.buy_shares(symbol, quantity)
        return f"Bought {quantity} shares of {symbol}. New holdings: {account.get_holdings()}"
    except ValueError as e:
        return str(e)

def sell_shares(symbol: str, quantity: int):
    if account is None:
        return "No account found. Please create an account first."
    try:
        account.sell_shares(symbol, quantity)
        return f"Sold {quantity} shares of {symbol}. New holdings: {account.get_holdings()}"
    except ValueError as e:
        return str(e)

def portfolio_value():
    if account is None:
        return "No account found. Please create an account first."
    return f"Total portfolio value: ${account.calculate_portfolio_value():.2f}"

def profit_loss():
    if account is None:
        return "No account found. Please create an account first."
    return f"Profit/Loss: ${account.get_profit_loss():.2f}"

def transactions():
    if account is None:
        return "No account found. Please create an account first."
    return account.get_transactions()

with gr.Blocks() as demo:
    gr.Markdown("## Trading Simulation Account Management")
    
    username_input = gr.Textbox(label="Username", placeholder="Enter your username")
    initial_deposit_input = gr.Number(
        label="Initial Deposit",
        placeholder="Enter your initial deposit amount",
        value=1000.0,
    )
    create_button = gr.Button("Create Account")
    output_create = gr.Textbox(label="Output", interactive=False)

    create_button.click(fn=create_account, inputs=[username_input, initial_deposit_input], outputs=output_create)

    deposit_input = gr.Number(label="Deposit Amount")
    deposit_button = gr.Button("Deposit")
    output_deposit = gr.Textbox(label="Output", interactive=False)

    deposit_button.click(fn=deposit, inputs=deposit_input, outputs=output_deposit)

    withdraw_input = gr.Number(label="Withdrawal Amount")
    withdraw_button = gr.Button("Withdraw")
    output_withdraw = gr.Textbox(label="Output", interactive=False)

    withdraw_button.click(fn=withdraw, inputs=withdraw_input, outputs=output_withdraw)

    buy_symbol_input = gr.Textbox(label="Symbol (e.g., AAPL, TSLA, GOOGL)")
    buy_quantity_input = gr.Number(label="Quantity")
    buy_button = gr.Button("Buy Shares")
    output_buy = gr.Textbox(label="Output", interactive=False)

    buy_button.click(fn=buy_shares, inputs=[buy_symbol_input, buy_quantity_input], outputs=output_buy)

    sell_symbol_input = gr.Textbox(label="Symbol (e.g., AAPL, TSLA, GOOGL)")
    sell_quantity_input = gr.Number(label="Quantity")
    sell_button = gr.Button("Sell Shares")
    output_sell = gr.Textbox(label="Output", interactive=False)

    sell_button.click(fn=sell_shares, inputs=[sell_symbol_input, sell_quantity_input], outputs=output_sell)

    portfolio_button = gr.Button("Check Portfolio Value")
    output_portfolio = gr.Textbox(label="Output", interactive=False)

    portfolio_button.click(fn=portfolio_value, inputs=[], outputs=output_portfolio)

    profit_loss_button = gr.Button("Check Profit/Loss")
    output_profit_loss = gr.Textbox(label="Output", interactive=False)

    profit_loss_button.click(fn=profit_loss, inputs=[], outputs=output_profit_loss)

    transactions_button = gr.Button("List Transactions")
    output_transactions = gr.Textbox(label="Output", interactive=False)

    transactions_button.click(fn=transactions, inputs=[], outputs=output_transactions)

if __name__ == "__main__":
    demo.launch()