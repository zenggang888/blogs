
#split,切割字符串，返回列表
print('abc'.split())
#['abc']
print('abcsbfsbmdnf'.split('b'))
#['a', 'cs', 'fs', 'mdnf']

#字符串格式化
print("my name is：%s,my age is:%d"%('jack',25))

#format可指定传的参数的index，不写默认按顺序
print("my name is：{0},my age is：{1}".format('jack',25))

#10个字符串，居中,五位数，还可以使用05f保留5位小数
print("my name is：{0:^10s},my age is：{1:05d}".format('jack',25))


