import pandas as pd
import os
import pprint
class Data:

    def __init__(self, job, topic):
        self.topic = topic
        self.columns = [str(i) for i in list(range(self.topic))]
        self.job_df = job
        # self.mbti_df = pd.read_csv("C:/Users/dusdm/PycharmProjects/pythonProject/softproject/user/modules/dataset/mbti_topic.csv")
        path = os.path.dirname(os.path.realpath(__file__))
        path = path.replace('\\', '/')

        self.mbti_df = pd.read_csv(path+"/dataset/mbti_topic.csv")


    def merge_rating_topic(self, rating):  # [cb] 사용자 평점 별 topic 데이터

        merge_df = pd.merge(rating, self.job_df)  # 사용자 평점 정보

        for i in self.columns:
            merge_df[i] = merge_df[i] * merge_df['rating'] * 0.2

        return merge_df


    # 직종 정보에 평점정보 추가하여 데이터 업데이트 안하기로 (21.11.09)
    # def make_job_mbti(self, rating):  # [cb] 직종 별 mbti수치 계산 (21.11.02)
    #
    #     input_df = rating
    #     data_list = []
    #
    #     for i in self.job_df['sub_code'].values:
    #         df = input_df[input_df['sub_code'] == i][self.columns]
    #         df = df.sum() / len(df)
    #         data_list.append([i] + df.values.tolist())
    #
    #     job_result_df = pd.DataFrame(data=data_list, columns=['sub_code', 'E', 'I', 'S', 'N', 'T', 'F', 'J', 'P']).fillna(0)
    #     #     job_result_df.to_csv("./dataset/job_mbti_values.csv", index=False, encoding='utf-8')
    #
    #     return job_result_df


    def make_user_mbti(self, rating, user, mbti):  # 한 사용자의 mbti 수치 계산

        # case 1. mbti 정보를 수치 일정 값으로 적용
        mbti_num = 10

        df1 = rating[rating['email'] == user]
        df2 = self.mbti_df[self.mbti_df['mbti'] == mbti].values[0]
        df2 = pd.DataFrame(data=[df2 for i in range(mbti_num)], columns=['mbti'] + self.columns)

        df = pd.concat([df1, df2])[self.columns]
        df = df.sum() / len(df)

        # print('make_user : ', df.values.tolist())

        return df.values.tolist()



if __name__ == "__main__":

    rating_df = pd.read_csv("./dataset/random_user_rating.csv")
    data = Data()

    rating = data.merge_rating_topic(rating_df)

    # print(data.mbti_df)

    a = data.make_user_mbti(rating,0)
    print(a)