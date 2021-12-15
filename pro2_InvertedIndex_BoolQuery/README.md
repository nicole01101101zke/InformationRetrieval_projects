首先运行create_index.py建立倒排索引

需要修改数据集所在路径，我的数据集路径：

```python
path1 = "D:\\大四上\\信息检索\\pro02\\data\\数据"
path2 = "D:/大四上/信息检索/pro02/data/数据/"
```

运行成功后得到文件dict.index.txt



再运行bool.py，可以进行布尔查询

支持输入X，X or Y，X and Y类型的布尔查询

输入为空会print("请输入内容\n")

若存在中间符号且中间符号不是or或者and，会print("输入不正确，请输入一个布尔查询Q （And Or 操作）")

若倒排索引表中没有该词项，会print("找不到结果...")

若输入 X and Y or Z，会返回X and Y的结果，忽略后面的任何内容

输入exit可以退出程序
