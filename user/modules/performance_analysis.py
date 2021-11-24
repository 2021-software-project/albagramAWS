# import pandas as pd
#
# from job_code import sub_code_list
# import make_sample
# from cb_data_preprocessing import Data
# from cb_contents_rec import *
# from cf_item_rec import Item
# from cf_user_rec import User
#
#
# class Analysis:
#
#     def __init__(self):
#         self.topic = 29
#         self.code_list = sub_code_list()
#
#         try:
#             # 학습 데이터 셋 = 사용자 평점 정보
#             rating_df = pd.read_csv(
#                 '../../../../../Downloads/mbti-based-job-recommend-main/mbti-based-job-recommend-main/dataset/random_user_rating.csv')
#         except:
#             make_sample.make_sample()
#             rating_df = pd.read_csv(
#                 '../../../../../Downloads/mbti-based-job-recommend-main/mbti-based-job-recommend-main/dataset/random_user_rating.csv')
#
#         self.train_df, self.test_df = train_test_split(rating_df, test_size=0.3, shuffle=True, random_state=121)
#         self.test_df = self.test_df[self.test_df['rating'] >= 4]
#
#         self.user_list = self.train_df['user_id'].drop_duplicates().values
#
#
#
#     def performance_analysis(self, algorithm, rec_num=5):
#
#         global rating, job, rec_list
#
#
#         if algorithm == 'cb':
#             data = Data(self.topic)
#             rating = data.merge_rating_topic(self.train_df)
#             # job = data.make_job_mbti(rating) # mbti 지표값 사용할때 씀
#             job = pd.read_csv("./dataset/job-topic_29_1.csv")
#
#         elif algorithm == 'cf_i':
#             item_cf = Item(self.train_df)
#             sim = item_cf.calc_item_simmularity()
#
#         elif algorithm == 'cf_u':
#             user_cf = User(self.train_df)
#             sim = user_cf.calc_user_simmularity()
#
#
#         k = rec_num  # 추천받을 직종 개수
#
#         indicator = [0, 0, 0, 0]  # accuracy, precision, recall, f1score
#         for user in self.user_list:
#             # print("사용자 ", user, "시작")
#             if algorithm == 'cb':
#                 user_model = data.make_user_mbti(rating, user)
#                 rec_list = contents_based_rec(user_model, job, self.topic, k)  # 추천 리스트
#
#             elif algorithm == 'cf_i':
#                 # sim_df = pd.read_csv("./dataset/item_simmularity.csv")
#                 rec_list = item_cf.item_based_rec(sim)
#
#             elif algorithm == 'cf_u':
#                 # sim_df = pd.read_csv("./dataset/user_simmularity.csv")
#                 rec_list = user_cf.user_based_rec(sim)
#
#
#             y_pred = pd.DataFrame(columns=self.code_list)
#             y_pred.loc[len(y_pred)] = [0 for i in range(150)]  # 초기화
#             y_pred[rec_list] = y_pred[rec_list].replace([0], 1)
#             y_pred = y_pred.values.tolist()[0]
#
#             real_list = self.test_df[self.test_df['user_id'] == user]['sub_code'].values.tolist()
#             y_true = pd.DataFrame(columns=self.code_list)
#             y_true.loc[len(y_true)] = [0 for i in range(150)]  # 초기화
#             y_true[real_list] = y_true[real_list].replace([0], 1)
#             y_true = y_true.values.tolist()[0]
#
#             indicator[0] += metrics.accuracy_score(y_true, y_pred)
#             indicator[1] += metrics.precision_score(y_true, y_pred)
#             indicator[2] += metrics.recall_score(y_true, y_pred)
#             indicator[3] += metrics.f1_score(y_true, y_pred)
#
#         #         metrics.classification_report(y_true, y_pred)
#         #         metrics.confusion_matrix(y_true, y_pred)
#
#         print("accuracy : ", indicator[0] / len(self.user_list))
#         print("precision : ", indicator[1] / len(self.user_list))
#         print("recall : ", indicator[2] / len(self.user_list))
#         print("f1 score : ", indicator[3] / len(self.user_list))
#
#
# if __name__ == "__main__":
#     ana = Analysis()
#
#     print("1. cb")
#     ana.performance_analysis('cb', 10)
#     print("2. cf_item based")
#     ana.performance_analysis('cf_i', 10)
#     print("3. cf_user based")
#     ana.performance_analysis('cf_u', 10)
