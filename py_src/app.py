from flask import Flask, render_template, request, redirect
import sys
sys.path += ['../']
from CmsLib import *

app = Flask(__name__ , template_folder = '../html_src/', static_folder = '../html_src/')
pysql = PySql(app, 'db.yaml')

@app.route('/', methods = ['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/InventoryManager', methods = ['GET', 'POST'])
def load_inventory_modules():
    if request.method == 'POST' :
        if 'add_product' in request.form:
            return redirect('InventoryManager/AddProduct')
        elif 'place_order' in request.form:
            return redirect('InventoryManager/PlaceOrder')
        elif 'receive_order' in request.form:
            return redirect('InventoryManager/ReceiveOrder')
        elif 'cancel_order' in request.form:
            return redirect('InventoryManager/CancelOrder')
        elif 'view_inventory' in request.form:
            return redirect('InventoryManager/ViewInventory')
        elif 'view_products' in request.form:
            return redirect('InventoryManager/ViewProducts')
        elif 'order_details' in request.form:
            return redirect('InventoryManager/OrderDetails')
        elif 'daily_orders' in request.form:
            return redirect('InventoryManager/DailyOrders')
        elif 'transaction_log' in request.form:
            return redirect('InventoryManager/TransactionLog')
        elif 'products_in_inv_transactions' in request.form:
            return redirect('InventoryManager/ProductsInInvTransactions')

    return render_template('/InventoryManager/inventory_manager_home.html')

@app.route('/InventoryManager/AddProduct', methods = ['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        product_id = request.form['product_id'].strip()
        name = request.form['name'].strip()
        description = request.form['description'].strip()
        unit_price = request.form['unit_price'].strip()
        unit_type = request.form['unit_type'].strip()
        current_discount = request.form['current_discount'].strip()
        ProductManager.add_product(pysql, product_id, name, description, unit_price, unit_type, current_discount)
        return redirect('../InventoryManager')
    else:
        return render_template('InventoryManager/add_product.html')

@app.route('/InventoryManager/PlaceOrder', methods = ['GET', 'POST'])
def place_order():
    product_ = ProductManager.get_all_products(pysql)
    product_data = [(each[0], each[1], each[4]) for each in product_]
    if request.method == 'POST':
        order_details = list()
        quantities = request.form.getlist("quantity[]")
        for i in range(len(product_)):
            if quantities[i]:
                quantity = float(quantities[i])

                if quantity:
                    order_details.append((product_[i][0], quantity))
        if order_details:
            order_id = OrderManager.place_order(pysql, order_details)
            return render_template('/InventoryManager/success_placed.html', order_id = order_id)
        else:
            return redirect('/InventoryManager')
    else:
        return render_template('/InventoryManager/place_order.html', product_data = product_data)

@app.route('/InventoryManager/ReceiveOrder', methods = ['GET', 'POST'])
def receive_order():
    if request.method == 'POST':
        order_id = request.form['order_id']
        OrderManager.receive_order(pysql, order_id)
        return redirect('/InventoryManager')
    else:
        return render_template('/InventoryManager/receive_order.html')

@app.route('/InventoryManager/CancelOrder', methods = ['GET', 'POST'])
def cancel_order():
    if request.method == 'POST':
        order_id = request.form['order_id'].strip()
        OrderManager.cancel_order(pysql, order_id)
        return redirect('/InventoryManager')
    else:
        return render_template('/InventoryManager/cancel_order.html')

@app.route('/InventoryManager/ViewInventory', methods = ['GET', 'POST'])
def view_inventory():    
    data = InventoryManager.get_inventory_details(pysql)
    return render_template('/InventoryManager/view_inventory.html', data=data)
    

@app.route('/InventoryManager/ViewProducts', methods = ['GET', 'POST'])
def view_products():
    data = ProductManager.get_all_products(pysql)
    return render_template('/InventoryManager/view_products.html', data=data)

@app.route('/InventoryManager/OrderDetails', methods = ['GET', 'POST'])
def order_details():
    if request.method == 'POST':
        order_id = request.form['order_id']
        order_status, order_details = OrderManager.get_order_details(pysql, order_id)
        return render_template('/InventoryManager/order_details.html', order_status=order_status, order_details=order_details)
    else:
        return render_template('/InventoryManager/order_details_home.html')

@app.route('/InventoryManager/DailyOrders', methods = ['GET', 'POST'])
def daily_orders():
    if request.method == 'POST':
        start_date, end_date = request.form['orders_from_date'], request.form['orders_to_date']
        order_details = OrderManager.get_orders_between_date(pysql, start_date, end_date)
        return render_template('/InventoryManager/day_specific_orders.html', order_details=order_details)
    else:
        return render_template('/InventoryManager/daily_orders_home.html')

@app.route('/InventoryManager/TransactionLog', methods = ['GET', 'POST'])
def transaction_log():
    transaction_details = InventoryManager.get_transactions(pysql)
    return render_template('/InventoryManager/inventory_transactions_log.html', transaction_details=transaction_details)

@app.route('/InventoryManager/ProductsInInvTransactions', methods = ['GET', 'POST'])
def transactions_of_product_on_date():
    products = ProductManager.get_all_products(pysql)
    products = [each[1] for each in products]
    if request.method == 'POST':
        on_date, product_name = request.form['transactions_on_date'], request.form['product_name']
        product_id = ProductManager.get_product_id_from_name(pysql, product_name)
        data = InventoryManager.get_transactions_of_product_by_date(pysql, product_id, on_date)
        return render_template('/InventoryManager/products_in_inv_transactions.html', data=data)
    else:
        return render_template('/InventoryManager/products_in_inv_transactions_home.html', products=products)

@app.route('/TokenManager', methods = ['GET', 'POST'])
def token_manager_home():
    if request.method == 'POST':
        if 'get_token_statuses' in request.form:
            return redirect('/TokenManager/Token_Statuses')
        elif 'get_token' in request.form:
            return redirect('/TokenManager/Get_Token')
        elif 'return_token' in request.form:
            return redirect('/TokenManager/Return_Token')
        elif 'get_token_details' in request.form:
            return redirect('/TokenManager/Get_Token_Details')
    else:
        return render_template('/TokenManager/token_manager_home.html')

@app.route('/TokenManager/Token_Statuses', methods = ['GET', 'POST'])
def token_statuses():
    statuses = TokenManager.get_all_tokens_status(pysql)
    print (statuses)
    '''for status in statuses :
        if status[1] == 0:
            status[1] = "No"
        else:
            status[1] = "Yes"'''
    return render_template('/TokenManager/token_statuses.html', statuses = statuses)

@app.route('/TokenManager/Get_Token', methods = ['GET', 'POST'])
def get_token():
    token_id = TokenManager.get_token(pysql)
    return render_template('/TokenManager/get_token.html', token_id = token_id)

@app.route('/TokenManager/Return_Token', methods = ['GET', 'POST'])
def return_token():
    if request.method == 'POST':
        token_id = request.form['token_id']
        TokenManager.put_token(pysql, token_id)
        return render_template('/TokenManager/successfully_returned.html')
    else:
        return render_template('/TokenManager/token_home.html')

@app.route('/TokenManager/Get_Token_Details', methods=['GET', 'POST'])
def get_token_details():
    if request.method == 'POST':
        token_id = request.form['token_id']
        token_details = TokenManager.get_token_details(pysql, token_id)
        return render_template('/TokenManager/get_token_details.html', token_details = token_details)
    else:   
        return render_template('/TokenManager/token_home.html')        

@app.route('/BillOperator', methods = ['GET', 'POST'])
def bill_operator_home():
    if request.method == 'POST' :
        if 'generate_invoice' in request.form:
            return redirect('BillOperator/GenerateInvoice')
        elif 'update_gst_cgst' in request.form:
            return redirect('BillOperator/UpdateCgstGst')
        elif 'additional_discount' in request.form:
            return redirect('BillOperator/AdditionalDiscount')
        elif 'view_invoice_details' in request.form:
            return redirect('BillOperator/ViewInvoice')
        elif 'date_wise_invoice' in request.form:
            return redirect('BillOperator/DateWiseInvoice')
    else:
	return render_template('/BillOperator/bill_operator_home.html')

if __name__ == "__main__" :
    app.run(debug = True)