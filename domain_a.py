import requests
from lxml import etree as ET
from concurrent.futures import ThreadPoolExecutor

def check_domain_availability(domain):
    #万网的域名查询接口，有别的接口也可以改。
    url = f'http://panda.www.net.cn/cgi-bin/check.cgi?area_domain={domain}'

    try:
        response = requests.get(url)
        if response.status_code == 200:
            returncode = None
            parser = ET.XMLParser(recover=True)
            root = ET.fromstring(response.content, parser=parser)
            #解析获取的接口字段returncode代表成功状态200
            returncode_element = root.find('returncode')
            # 解析获取的接口字段key代表域名
            key_element = root.find('key')
            # 解析获取的接口字段original代表域名状态
            original_element = root.find('original')

            if returncode_element is not None and key_element is not None and original_element is not None:
                returncode = returncode_element.text
                key = key_element.text
                original = original_element.text

            if returncode == '200':
                if "210 : Domain name is available" in original:
                    result = f"{key} 未被注册"
                elif "211 : Domain exists" in original or "211 : Platinum Reserved" in original or "211 : Reserved Domain Name" in original:
                    #如果只想输出能够注册的域名可以把result改为空。 result = ""
                    result = f"{key} 已被注册"
                else:
                    result = f"无法确定 {key} 的注册状态"
            else:
                result = f"API请求失败，返回码: {returncode}"
        else:
            result = f"HTTP请求失败，状态码: {response.status_code}"
    except Exception as e:
        result = f"发生错误: {str(e)}"

    if result and result.strip():
        print(result)
    return result

def check_domains_availability(domain_list):
    #max_workers是线程数，1最稳定，越大越不稳定，但是速度越快之后报错越多。除非你超级计算机。
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(check_domain_availability, domain_list))
    return results

def read_domain_list_from_file(file_path):
    with open(file_path, 'r') as file:
        domain_list = [line.strip() for line in file if line.strip()]
    return domain_list

def write_results_to_file(results, output_file):
    with open(output_file, 'w') as file:
        for result in results:
            file.write(result + '\n')

# 从输入文件中读取域名列表
input_file_path = '2com.txt'
domain_list = read_domain_list_from_file(input_file_path)

# 批量查询域名状态（多线程）
results = check_domains_availability(domain_list)

# 将结果写入输出文件
output_file_path = 'output.txt'
write_results_to_file(results, output_file_path)
