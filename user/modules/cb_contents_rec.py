import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def contents_based_rec(user_model, job, topic, k=5):
    rec_num = k  # 추천받을 직종 개수

    sim = [[0, 0.0] for x in range(166)]
    # print(job)
    for index, row in job.iterrows():
        sim[index][0] = row[1]

        user_model = np.array(user_model).reshape(1, topic)
        row = row[2:].to_numpy().reshape(1, topic)
        sim[index][1] = cosine_similarity(user_model, row)[0][0]

    sim = sorted(sim, key=lambda x: x[1], reverse=True)
    # print(sim)



    rec_job = []
    for num in sim[:rec_num]:
        rec_job.append(num[0])

    # print(rec_job)
    return rec_job


if __name__ == "__main__":
    import pandas as pd
    user_model = [0.012230593680000002, 0.02916013316, 0.01274666418, 0.03226582911999999, 0.020360821140000002, 0.0060966156799999996, 0.00809303818, 0.053509504740000005, 0.01030679318, 0.01590789268, 0.01194157618, 0.00419278068, 0.022110812520000002, 0.00753545318, 0.007693972679999999, 0.006586494180000001, 0.009933660680000001, 0.00994330668, 0.057323831879999995, 0.01018097768, 0.01331180518, 0.01060514568, 0.00720134018, 0.00593063568, 0.01200419418, 0.040153303599999995, 0.08036605356000001, 0.01328731518, 0.01350565668]
    job = pd.read_csv("./dataset/job-topic_29_1.csv")

    contents_based_rec(user_model, job, 29, k=5)