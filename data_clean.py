import pandas as pd

# 读取CSV文件
data = pd.read_csv("data/Online_Retail_500.csv")
# # 不缩减列的显示宽度
# pd.set_option('display.max_columns', None)
# # 打印所有行和列
# pd.set_option('display.max_rows', None)

# 1.1 了解数据情况
# 1）读取前6行和后6行数据
first_6_rows = data.head(6)
last_6_rows = data.tail(6)
# 打印结果
print("前6行数据:")
print(first_6_rows)
print("\n后6行数据:")
print(last_6_rows)

# 2）数据的基本信息
num_records = data.shape[0]  # 记录数
num_fields = data.shape[1]  # 字段数
field_names = data.columns.tolist()  # 字段名
data_types = data.dtypes  # 字段数据类型
# 打印结果
print("\n数据基本信息:")
print("记录数：", num_records)
print("字段数：", num_fields)
print("字段名：", field_names)
print("\n字段数据类型:")
print(data_types)

# 3）空值情况
null_counts = data.isnull().sum()  # 统计每个字段的空值数量
# 打印结果
print("\n空值情况:")
print(null_counts)

# 4）数据集的分布情况
data_statistics = data.describe()
# 打印结果
print("\n数据集的分布情况:")
print(data_statistics)

# 1.2 数据清洗和整理
# 1）删除含有空值的记录
data_cleaned = data.dropna()

# 2）数据类型转换
data_cleaned = data_cleaned.copy()  # 创建一个副本，并在副本上进行操作，不然会一直警告
data_cleaned['InvoiceDate'] = pd.to_datetime(data_cleaned['InvoiceDate'])  # 将InvoiceDate字段转换为日期类型
data_cleaned['Description'] = data_cleaned['Description'].str.lower()  # 将Description字段中的字符串内容转换为小写
data_cleaned['CustomerID'] = data_cleaned['CustomerID'].astype(int)  # 将CustomerID字段转换为整数类型

# 3）添加新数据
data_cleaned['AmountSpent'] = data_cleaned['UnitPrice'] * data_cleaned['Quantity']  # 计算消费总金额字段
data_cleaned['Month'] = data_cleaned['InvoiceDate'].dt.month  # 提取月份
data_cleaned['DayOfWeek'] = data_cleaned['InvoiceDate'].dt.dayofweek  # 提取星期几，0表示星期一，1表示星期二，以此类推
data_cleaned['Hour'] = data_cleaned['InvoiceDate'].dt.hour  # 提取小时

# 4）另存为新的CSV文件
data_cleaned.to_csv("data/Online_Retail_Clean.csv", index=False)

# 打印处理后的数据
print("处理后的数据：")
print(data_cleaned)
