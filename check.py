from src import utils
from src import checker
import argparse
import logging
from getpass import getpass

def get_args():
    SupportJudges = ['vj', 'nc', 'jsk', 'cf', 'atc']

    parser = argparse.ArgumentParser(description='Crawling the contest information')
    parser.add_argument('-o', type=str, help='The Name of the OJ to crawl', 
                        required=True, choices=SupportJudges)
    parser.add_argument('-c', type=int, help='The Contest ID', required=True)
    parser.add_argument('-n', type=int, help='The Number of Problems', default=13)

    return parser.parse_args()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    args = get_args()

    # 用户账号
    user = utils.get_user(args.o)

    # 提交记录
    if args.o == 'vj':
        username = input("login username: ")
        password = getpass("login password: ")
        cookies = utils.login(username, password)  
        json = utils.get_contest(args.o, args.c, cookies)
    else:
        json = utils.get_contest(args.o, args.c)

    # 统计ac数
    if args.o == 'nc':
        data, endTime = utils.fliter(json, user)
        # utils.after_solve(data, user, args.c, endTime)
    elif args.o == 'vj':
        data = None

    result = checker.check(data, args.n, './config/nowcoder.xlsx')
    cnt = 0
    while True:
        try:
            result.save("result" + str(cnt) + ".xlsx")
            logging.info("Save result at result.xlsx")
            break
        except Exception as e:
            print('error ', str(e))
            print('try again')
            cnt += 1
