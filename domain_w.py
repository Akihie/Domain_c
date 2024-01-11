import time
import whois
import threading

def check_domain_availability(domain_name, results):
    try:
        domain_info = whois.whois(domain_name)
        if domain_info.status == None:
            result = f"{domain_name} 未被注册"
        else:
            #不想输出已被注册的可以改为result = ""
            result = f"{domain_name} 已被注册"
    except whois.parser.PywhoisError:
        result = f"查询 {domain_name} 时发生错误"

    results.append(result)
    print(result)

def main():
    # 从输入文件中读取域名列表
    input_file_path = "2com.txt"
    # 输出文件域名列表
    output_file_path = "output.txt"

    with open(input_file_path, "r") as input_file:
        domain_list = [line.strip() for line in input_file.readlines()]

    # 创建一个列表来保存查询结果
    results = []

    # 创建线程列表
    threads = []

    # 限制并发线程数量
    max_threads = 10  # 你可以根据需要调整这个值

    # 使用多线程进行域名查询
    for domain in domain_list:
        thread = threading.Thread(target=check_domain_availability, args=(domain, results))
        threads.append(thread)
        thread.start()
        #加个延迟，不过感觉好像没什么用，调线程就可以了
        # time.sleep(1)  # 增加1秒延迟

    # 等待所有线程完成
    for thread in threads:
        thread.join()

    # 将查询结果写入输出文件
    with open(output_file_path, "w") as output_file:
        for result in results:
            output_file.write(result + "\n")

if __name__ == "__main__":
    main()
