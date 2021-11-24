from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
import os

class User :
    def __init__(self, rating):
        self.rating = rating


    def calc_user_simmularity(self):
        pivot_df = pd.pivot_table(self.rating, index=['email'], columns='sub_code',
                                  fill_value=0)  # 평가 안한 직종 0 (평점 1~5)
        user_sim_df = pd.DataFrame(cosine_similarity(pivot_df, pivot_df))

        # user_sim_df.to_csv("./dataset/user_simmularity.csv", index=False, encoding='utf-8')

        return user_sim_df

    def user_based_rec(self, sim_df, target_user=0, k=5):
        user = target_user  # 추천받을 유저 (입력)
        rec_num = k

        # index, column명 사용자 이름으로 변경
        sim_df.index = self.rating['email'].drop_duplicates()
        sim_df.columns = self.rating['email'].drop_duplicates()

        # 평가된 전체 업직종
        total_job = list(sorted(set(self.rating['sub_code'])))

        user_data = self.rating[self.rating['email'] == user]['sub_code'].tolist()  # 해당 사용자가 평가한 직종
        user_job_data = sorted(list(set(total_job) - set(user_data)))  # 해당 사용자가 평가하지 않은 직종

        rec_job = [] # 최종 추천될 K개 직종

        # 해당 사용자가 평가하지 않은 직종 중에서 추천 (직종 코드 한개씩 반복)
        for item in user_job_data:

            job_i = self.rating[self.rating['sub_code'] == item]
            sim_i = sim_df.loc[user, job_i['email']].values
            if sim_i.sum() != 0:
                r = np.dot(sim_i, job_i['rating'].values) / sim_i.sum()  # 예상평점 계산

                rec_job.append((item, r))
                # print("rec_job ",rec_job)

        rec_job.sort(key=lambda x: x[1], reverse=True)

        rec_list = []
        for num in rec_job[:rec_num]:
            rec_list.append(num[0])

        return rec_list


if __name__ == "__main__":

    path = "../../../../../Downloads/mbti-based-job-recommend-main/mbti-based-job-recommend-main/dataset"
    if not os.path.isdir(path):
        os.mkdir(path)

    rating_df = pd.read_csv(
        '../../../../../Downloads/mbti-based-job-recommend-main/mbti-based-job-recommend-main/dataset/random_user_rating.csv')

    user = User(rating_df)
    sim = user.calc_user_simmularity()
    rec_job_list = user.user_based_rec(sim)

    print(rec_job_list)