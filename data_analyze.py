from pyecharts.charts import Bar, Line, Page, Pie
from pyecharts import options as opts
from pyecharts.globals import ThemeType
import pandas as pd

# 这里需要指明"InvoiceDate"列是日期时间类型，不然这列数据会被解释为字符串类型
data = pd.read_csv("data/Online_Retail_Clean.csv", parse_dates=["InvoiceDate"])
data = data.copy()  # 创建一个副本，并在副本上进行操作，不然会一直警告（因为python中的“变量”其实是一个“标签”，而不是一个“容器”）


# 1) 查询订单量最大的前5个用户
print("1) 查询订单量最大的前5个用户")
top_users_orders = data.groupby(['CustomerID', 'Country'])['Quantity'].sum().nlargest(5).reset_index()
print(top_users_orders)

# 2) 查询消费金额最多的前5个用户
print("2) 查询消费金额最多的前5个用户")
top_users_spending = data.groupby(['CustomerID', 'Country'])['AmountSpent'].sum().nlargest(5).reset_index()
print(top_users_spending)

# 3) 按年统计订单和金额，并绘制折线图。（订单和金额呈上升趋势，销售趋势从2010-2011呈递增趋势）
yearly_sales = data.groupby(data['InvoiceDate'].dt.year)[['Quantity', 'AmountSpent']].sum()
line_chart = (
    Line(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
    .add_xaxis(yearly_sales.index)
    .add_yaxis("Order Quantity", yearly_sales['Quantity'].tolist())
    .add_yaxis("Sales Amount", yearly_sales['AmountSpent'].tolist())
    .set_global_opts(
        title_opts=opts.TitleOpts(title="Yearly Sales"),
        xaxis_opts=opts.AxisOpts(type_="category", name="Year"),
        yaxis_opts=opts.AxisOpts(type_="value", name="Amount"),
    )
    .add_js_funcs("""
      document.write("<div style='text-align:left;font-size:24px;margin-top:20px;'>由图可见，订单和金额呈上升趋势，销售趋势从2010-2011呈递增趋势。</div>")
    """)
)

# 4) 按月统计订单数量，并绘制柱状图
monthly_orders = data.groupby(data['Month'])['Quantity'].sum()
bar_chart_monthly = (
    Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
    .add_xaxis(monthly_orders.index.tolist())
    .add_yaxis("Order Quantity", monthly_orders.tolist())
    .set_global_opts(
        title_opts=opts.TitleOpts(title="Monthly Order Quantity"),
        xaxis_opts=opts.AxisOpts(type_="category", name="Month"),
        yaxis_opts=opts.AxisOpts(type_="value", name="Quantity"),
    )
    .add_js_funcs("""
        document.write("<div style='text-align:left;font-size:24px;margin-top:20px;'>由上图可以看出，1月份订单量最多达到3065，其次是12月份的2376，之后是2月份的48。</div>")
    """)
)

# 5) 按日统计订单数量，并绘制柱状图
daily_orders = data.groupby(data['InvoiceDate'].dt.day)['Quantity'].sum()
bar_chart_daily = (
    Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
    .add_xaxis(daily_orders.index.tolist())
    .add_yaxis("Order Quantity", daily_orders.tolist())
    .set_global_opts(
        title_opts=opts.TitleOpts(title="Daily Order Quantity"),
        xaxis_opts=opts.AxisOpts(type_="category", name="Day"),
        yaxis_opts=opts.AxisOpts(type_="value", name="Quantity"),
    )
    .add_js_funcs("""
        document.write("<div style='text-align:left;font-size:24px;margin-top:20px;'>由图可以看出，在每月的1、9、11号订单数据较多超过了600，12号与25号订单数量超过了400，其余时间段订单数量在0至400不等。</div>")
    """)
)

# 6) 按时统计订单数量，并绘制柱状图
hourly_orders = data.groupby(data['Hour'])['Quantity'].sum()
bar_chart_hourly = (
    Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
    .add_xaxis(hourly_orders.index.tolist())
    .add_yaxis("Order Quantity", hourly_orders.tolist())
    .set_global_opts(
        title_opts=opts.TitleOpts(title="Hourly Order Quantity"),
        xaxis_opts=opts.AxisOpts(type_="category", name="Hour"),
        yaxis_opts=opts.AxisOpts(type_="value", name="Quantity"),
    )
    .add_js_funcs("""
        document.write("<div style='text-align:left;font-size:24px;margin-top:20px;'>由上图我们可以发现，在[0-7]、[18-21]时间区间内，无销售数量。上午时间段，销售数量在递增，下午至傍晚时间段，销售数量在递减，其中在中午11点时销售数量最高，在早上8点也有一波购买热潮。</div>")
    """)
)

# 7）分析不同国家的订单数量和销售金额。
country_data = data.groupby("Country").agg({"InvoiceNo": "count", "AmountSpent": "sum"}).reset_index()
country_data = country_data.sort_values("InvoiceNo", ascending=False)

# 绘制订单数量柱状图
bar_chart_country = (
    Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
    .add_xaxis(country_data["Country"].tolist())
    .add_yaxis("Order Quantity", country_data["InvoiceNo"].tolist())
    .set_global_opts(
        title_opts=opts.TitleOpts(title="Order quantity in different countries"),
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-30), type_="category", name="Country"),
        yaxis_opts=opts.AxisOpts(type_="value", name="Quantity")
    )
    .add_js_funcs("""
        document.write("<div style='text-align:left;font-size:24px;margin-top:20px;'>由上图可以发现，英国的订单数量遥遥领先达到308。紧接其后的是德国和法国，24。然后其余的国家订单数量不超过10个。</div>")
    """)
)

# 绘制销售金额饼图
pie_chart_country = (
    Pie(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
    .add("", [list(z) for z in zip(country_data["Country"].tolist(), country_data["AmountSpent"].tolist())])
    .set_global_opts(
        title_opts=opts.TitleOpts(title="Sales amount in different countries"),
        legend_opts=opts.LegendOpts(
            type_="scroll", pos_top="20%", pos_left="90%", orient="vertical"
        ),
    )
    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    .add_js_funcs("""
        document.write("<div style='text-align:left;font-size:24px;margin-top:20px;'>由上图可以发现，英国的订单数量仍然遥遥领先，占比大半，为6526.71。紧接其后的是西班牙，有2928.96。然后是法国和德国，分别是887.24和473.64。之后的其余国家占比不到总销售金额的30%。</div>")
    """)
)

# 创建页面对象
page = Page(page_title="Data Analysis")

# 添加图表到页面
page.add(line_chart)
page.add(bar_chart_monthly)
page.add(bar_chart_daily)
page.add(bar_chart_hourly)
page.add(bar_chart_country)
page.add(pie_chart_country)

# 保存页面为HTML文件
page.render("data_analysis.html")
