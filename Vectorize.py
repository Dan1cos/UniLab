import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import pickle

def thirdSt(df_for_predict, df_for_dict):
    docs = df_for_dict['report_text'].tolist()

    cv = CountVectorizer(max_df=0.98, min_df=2)
    word_count_vector = cv.fit_transform(docs)

    with open("isw_parsed_3/count_vectorizer.pkl", "wb") as handle:
        pickle.dump(cv, handle)

    tfidf_transformer = TfidfTransformer()
    tfidf_transformer.fit(word_count_vector)

    df_idf = pd.DataFrame(tfidf_transformer.idf_, index=cv.get_feature_names_out(), columns=["idf_weights"])
    df_idf.sort_values(by=["idf_weights"])

    tf_idf_vector = tfidf_transformer.transform(word_count_vector)

    def sort_coo(coo_matrix):
        tuples = zip(coo_matrix.col, coo_matrix.data)
        return sorted(tuples, key=lambda x:(x[1], x[0]), reverse=True)

    def extract_topn_from_vector(feature_names, sorted_items, topn=10):
        sorted_items = sorted_items[:topn]

        score_vals = []
        feature_vals = []

        for idx, score in sorted_items:
            score_vals.append(round(score,3))
            feature_vals.append(feature_names[idx])

        results = {}
        for idx in range(len(feature_vals)):
            results[feature_vals[idx]]=score_vals[idx]
        return results

    def convert_to_vector(doc):
        feature_names = cv.get_feature_names_out()
        top_n = 100
        tf_idf_vector = tfidf_transformer.transform(cv.transform([doc]))

        sorted_items = sort_coo(tf_idf_vector.tocoo())

        keywords = extract_topn_from_vector(feature_names,sorted_items, top_n)

        return keywords

    keywords = df_for_predict['report_text'].apply(lambda x: convert_to_vector(x))
    return keywords
