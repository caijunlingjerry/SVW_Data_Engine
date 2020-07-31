
#Project B：产品关联分析
#现在需要你使用Apriori算法，挖掘订单中的频繁项集及关联规则
#数据源：产品表.csv，订单表.csv，客户.csv，日期表.csv

import pandas as pd
import time
# 数据加载
data = pd.read_csv('./订单表.csv',encoding='gbk')
df = data[['客户ID', '产品名称']].sort_values('客户ID')

#print(df)
hot_encoded_df=data.groupby(['客户ID','产品名称'])['产品名称'].count().unstack().reset_index().fillna(0).set_index('客户ID')
#print(hot_encoded_df)


# 采用efficient_apriori工具包
def rule1 ( ):
	from efficient_apriori import apriori
	start = time.time ( )
	# 得到一维数组orders_series，并且将Transaction作为index, value为Item取值
	orders_series = df.set_index ( '客户ID' )['产品名称']
	# 将数据集进行格式转换
	transactions = []
	temp_index = 0
	for i, v in orders_series.items ( ):
		if i != temp_index:
			temp_set = set ( )
			temp_index = i
			temp_set.add ( v )
			transactions.append ( temp_set )
		else:
			temp_set.add ( v )
		# 挖掘频繁项集和频繁规则
	itemsets, rules = apriori ( transactions, min_support=0.02, min_confidence=0.5 )
	print ( 'efficient_apriori频繁项集1：', itemsets )
	print ( 'efficient_apriori关联规则1：', rules )

	end = time.time ( )
	print ( "用时：", end - start )

def encode_units (x):
	if x <= 0:
		return 0
	if x >= 1:
		return 1

# 采用mlxtend.frequent_patterns工具包
def rule2 ( ):
	from mlxtend.frequent_patterns import apriori
	from mlxtend.frequent_patterns import association_rules
	pd.options.display.max_columns = 100
	start = time.time ( )
	hot_encoded_df = df.groupby ( ['客户ID', '产品名称'] )['产品名称'].count ( ).unstack ( ).reset_index ( ).fillna (
		0 ).set_index ( '客户ID' )
	#print ( hot_encoded_df )
	hot_encoded_df = hot_encoded_df.applymap ( encode_units )
	frequent_itemsets = apriori ( hot_encoded_df, min_support=0.03, use_colnames=True )
	rules = association_rules ( frequent_itemsets, metric="lift", min_threshold=0.5 )
	print ( "mlxtend频繁项集2：", frequent_itemsets )
	print ( "mlxtend关联规则2：", rules[(rules['lift'] >= 1) & (rules['confidence'] >= 0.5)] )
	# print(rules['confidence'])
	end = time.time ( )
	#print ( "用时：", end - start )

if __name__ == '__main__':
	rule1 ( )
	print ( '-' * 100 )
	rule2 ( )

