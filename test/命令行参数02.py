import argparse

parent_parser = argparse.ArgumentParser(add_help=False)
b = parent_parser.add_argument("--parent", type=int)
print(b)

foo_parser = argparse.ArgumentParser(parents=[parent_parser])
b = foo_parser.add_argument('foo')
print(b)

parser = argparse.ArgumentParser(prefix_chars="+")
b = parser.add_argument("+f")
print(b)

parser.add_argument("++bar")
b = parser.parse_args("+f X ++bar Y".split())
print(b)

with open('args.txt', 'w') as fp:
    fp.write('-f\nbar')
parser = argparse.ArgumentParser(fromfile_prefix_chars='@')
parser.add_argument('-f')
b = parser.parse_args(['-f', 'foo', '@args.txt'])
print(b)

parser = argparse.ArgumentParser()
parser.add_argument('--foo', action='store_const', const=42)
# b = parser.parse_args('--foo 34'.split())
# print(b.foo)

parser = argparse.ArgumentParser()
parser.add_argument('--foo', action='store_true')
parser.add_argument('--bar', action='store_false')
b = parser.parse_args('--foo --bar'.split())
print(b)

b = parser.parse_args('--foo --bar'.split())
print(b)

parser = argparse.ArgumentParser()
parser.add_argument('--foo', action='append')
c = '--foo 1 --foo 2  --foo 55555'.split()
print(c)
b = parser.parse_args('--foo 1 --foo 2  --foo 55555'.split())
print(b)

parser = argparse.ArgumentParser()

print('action=’count’ 统计该参数出现的次数')
parser = argparse.ArgumentParser()
parser.add_argument('--verbose', '-v', action='count')
c = '-vvv'.split()
print(c)
b = parser.parse_args('-vvv'.split())
print(b)

print('N (整数) N个命令行参数被保存在一个list中')
parser = argparse.ArgumentParser()
parser.add_argument('--foo', nargs=2)
parser.add_argument('bar', nargs=1)
c = 'c --foo a b'.split()
print(c)
b = parser.parse_args('c --foo a b'.split())
print(b)

print('通过指定type,可以对命令行参数执行类型检查和类型转换。通用的内置类型和函数可以直接用作type参数的值：')
parser = argparse.ArgumentParser()
parser.add_argument('foo', type=int)
parser.add_argument('bar', type=open)
b = parser.parse_args('2 temp.txt'.split())
print(b)
