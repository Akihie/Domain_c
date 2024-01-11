from itertools import product

def generate_combinations():
    # 生成所有英文组合，随意更改，想生成123abc的所有组合也可以
    letters = 'abcdefghijklmnopqrstuvwxyz'
    #repeat=后边为生成的位数，2代表生成2位前缀的域名。例如：ab.com
    combinations = [''.join(p) for p in product(letters, repeat=2)]
    return combinations

def write_to_txt(combinations, filename='2com.txt'):
    # 将组合写入txt文件
    with open(filename, 'w') as file:
        for combination in combinations:
            #.com代表生成.com后缀的域名
            file.write(combination + '.com\n')

if __name__ == "__main__":
    all_combinations = generate_combinations()
    write_to_txt(all_combinations)
