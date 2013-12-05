# puke 唐山打储
====

这是一个唐山扑克游戏，俗称打储，客户端为html5,服务器端采用ffrpc+python实现,通讯协议使用thrift的json。
## Feature
* 谁先拿到A，可以宣战，宣战后分数翻倍，并且和拥有同样花色A的为队友。宣战的A比2大.
* 大于等于3张即可出顺
* 3张同样的即可作为炸弹
* 宣战之后，对方可以投降，也可翻倍，称之为拧!

## Design
* Client 为web实现
* jquery + crafty
* server: ffrpc + python
* protocol: thrift  & json



