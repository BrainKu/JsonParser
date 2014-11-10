1. 实现了基本要求和进阶要求
2. 当读入的json串不符合语法时，会抛出ValueError异常，异常中包括对应的错误信息
3. 在读入文件时，默认是使用uft8编码
4. 测试文件包含两个，FailTest中所有的用例均会抛出ValueError异常，JsonParserTest中针对需要的函数分别写了对应的测试。
    运行请直接执行python + 文件名

备注：用例来自python内置库中的测试，非原创