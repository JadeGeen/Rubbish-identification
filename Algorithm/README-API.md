# API定义

## ALG FOR USER

```python
Algorithm.api(target, contra, base)
input : {
    target : ndarray #目标图片
    contra : bool #是否采用对比，若采用则contra为true，输入基准图和目标图，否则contra为false，输入目标图即可
    base : ndarray #基准图片
}
output : {
    target : ndarray #目标图片
    res : dict{list[], str} #图片信息，返回一个字典，分别为切割信息及切割部分标签
}
```