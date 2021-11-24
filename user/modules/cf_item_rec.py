from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
import os

class Item :
    def __init__(self, rating):
        self.rating = rating

    def calc_item_simmularity(self):
        pivot_df = pd.pivot_table(self.rating, index=['sub_code'], columns='email', fill_value=0)
        item_sim_df = pd.DataFrame(cosine_similarity(pivot_df, pivot_df))

        # item_sim_df.to_csv('./dataset/item_simmularity.csv', index=False, encoding='utf-8')

        return item_sim_df

    def item_based_rec(self, sim_df, target_user=0, k=5):
        user = target_user  # 추천받을 유저
        rec_num = k  # 추천받을 직종 개수

        sim_df.index = self.rating['sub_code'].drop_duplicates()
        sim_df.columns = self.rating['sub_code'].drop_duplicates()

        total_job = list(sorted(set(self.rating['sub_code'])))  # 평가된 전체 업직종

        rated_job_list = self.rating[self.rating['email'] == user]['sub_code'].tolist()  # 해당 사용자가 평가한 직종
        unrated_job_list = sorted(list(set(total_job) - set(rated_job_list)))  # 해당 사용자가 평가하지 않은 직종

        rec_job = []  # 최종 추천될 K개 직종

        # 해당 사용자가 평가하지 않은 직종 중에서 추천 (한개씩) - item, user 공통
        for item in unrated_job_list:

            job_i = self.rating[self.rating['email'] == user]  # 사용자가 평가한 업직종
            sim_i = sim_df.loc[item, job_i['sub_code']].values

            if sim_i.sum() != 0:
                r = np.dot(sim_i, job_i['rating'].values) / sim_i.sum()  # 예상평점 계산

                rec_job.append((item, r))

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

    item = Item(rating_df)
    sim = item.calc_item_simmularity()
    rec_job_list = item.item_based_rec(sim)

    print(rec_job_list)
