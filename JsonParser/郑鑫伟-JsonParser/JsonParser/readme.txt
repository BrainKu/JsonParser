1. 实现了基本要求和进阶要求
2. 当读入的json串不符合语法时，会抛出ValueError异常，异常中包括对应的错误信息
3. 在读写文件时，使用uft8编码
4. 单元测试文件包含2个，均可以在命令行中使用python执行。
FailTest中所有的用例均会抛出ValueError异常。
JsonParserTest中针对需要的函数分别写了测试，excel文档中的测试对应于test_main函数。