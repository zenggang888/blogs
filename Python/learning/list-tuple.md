- 元组不可变

- 列表可变

  

**创建元组的方式：**

```
t = (1,2,3) 或
t = 1,2,3
```

**创建列表的方式：**

```
l = [1,2,3] 或
l = list(1,2,3)
```
**两种创建列表的方式性能上还是有差距的,[]比list()更快，因为调用list函数有一定的开销**

**常用方法：**

都支持切片、索引查询、都可以随意嵌套、部分内置方法一致

```
>>> l = [3, 2, 3, 7, 8, 1]
>>> l.count(3) #统计元素数量
2

>>> l.index(7) #查索引
3

>>> l.reverse()  #反转
>>> l
[1, 8, 7, 3, 2, 3]

>>> l.sort() #排序
>>> l
[1, 2, 3, 3, 7, 8]

>>> tup = (3, 2, 3, 7, 8, 1)
>>> tup.count(3)
2

>>> tup.index(7)
3

>>> list(reversed(tup))
[1, 8, 7, 3, 2, 3]

>>> sorted(tup)
[1, 2, 3, 3, 7, 8]
```



**比较：**

一个空列表的空间是40字节

```
>>> l = []
>>> l.__sizeof__()
40
```

添加一个元素变成了72字节，因为int类型是8字节，列表会提前分配一定的空间，用完了继续提前分配，提高插入效率

```
>>> l.append(1)
>>> l.__sizeof__()
72
```

**元组性能要比列表高：**
初始化一个列表和元组：如果元素比较多，差距会大一些

```
zgdeMacBook-Pro:~ zg$ python -m timeit -s 'x=[1,2,3,4,5,6]' 
20000000 loops, best of 5: 9.93 nsec per loop

zgdeMacBook-Pro:~ zg$ python -m timeit -s 'x=(1,2,3,4,5,6)' 
50000000 loops, best of 5: 9.21 nsec per loop
```

索引操作，两者没有什么差距，可以忽略不计

```
zgdeMacBook-Pro:~ zg$ python -m timeit -s 'x=[1,2,3,4,5,6]' 'y=x[3]'
10000000 loops, best of 5: 31.3 nsec per loop

zgdeMacBook-Pro:~ zg$ python -m timeit -s 'x=(1,2,3,4,5,6)' 'y=x[3]'
10000000 loops, best of 5: 31.9 nsec per loop
```

