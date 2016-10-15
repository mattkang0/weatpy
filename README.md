**weatpy** 是一个命令行天气预报. 是wego的python实现. 
该项目仅用于学习用途.

![Screenshots](https://github.com/mattkang0/weatpy/blob/master/weatpy.png)

## 依赖
- osx或linux系统
- 终端为utf-8且支持256色
- 等宽字体
- 天气预报的API key. 前往 https://developer.forecast.io/register 注册.

## 安装
`pip install git+https://github.com/mattkang0/weatpy`

## 配置
安装后会创建~/.weatpyrc配置文件, 请根据自己需求进行配置

## 使用
```shell
$ weatpy 深圳
$ weatpy 深圳 -v 
$ weatpy 深圳 -vv
$ weatpy 22.5333,114.1333
$ weatpy -h
```


