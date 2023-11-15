# -*- coding: utf-8 -*-

import streamlit as st
import numpy as np
import pandas as pd
import altair as alt

st.write("Prediction Accuracy by base rate")

baserate = st.slider(label="Baserate", min_value=0.0, max_value=1.0, step=0.01)

sensitivity = st.slider(label="Sensitivity", min_value=0.01, max_value=1.0, step=0.01)
specificity = st.slider(label="Specificity", min_value=0.01, max_value=1.0, step=0.01)

sum_rr = baserate
sum_rn = 1-baserate

fn = (1-sensitivity) * sum_rr
tp = sum_rr * sensitivity

fp = (1-specificity)*sum_rn
tn = sum_rn * specificity

contingency = pd.DataFrame(np.array([[tp,fp,tp+fp],[fn,tn,fn+tn],[sum_rr,sum_rn,tp+fp+tn+fn]]), index=["Predicted Recidivism", "Predicted Non-Recidivism", "Sum"], columns=["Real Recidivism", "Real Non-Recidivism", "Sum"])


ppv = tp / (tp+fp)
npv = tn / (tn+fn)
acc = tp+tn

st.table(contingency)

st.write("Test Accuracy:", "{:.2f}".format(acc))
st.write("Positive Predictive Value: ", "{:.2f}".format(ppv))
st.write("Negative Predictive Value: ", "{:.2f}".format(npv))

n_total = 100

graphdata = pd.DataFrame([dict(id=i) for i in range (1, n_total+1)])
graphdata["Prediction Result"] = ""
n_fn = round(fn * n_total)
n_tp = round(tp * n_total)
n_fp = round(fp * n_total)
n_tn = round(tn * n_total)

graphdata["Prediction Result"].iloc[:n_tp] = "Correct Recidivism"
graphdata["Prediction Result"].iloc[n_tp:n_tp+n_fn] = "Wrong Non-Recidivism"
graphdata["Prediction Result"].iloc[n_tp+n_fn:n_tp+n_fn+n_fp] = "Wrong Recidivism"
graphdata["Prediction Result"].iloc[n_tp+n_fn+n_fp:] = "Correct Non-Recidivism"


person = (
    "M1.7 -1.7h-0.8c0.3 -0.2 0.6 -0.5 0.6 -0.9c0 -0.6 "
    "-0.4 -1 -1 -1c-0.6 0 -1 0.4 -1 1c0 0.4 0.2 0.7 0.6 "
    "0.9h-0.8c-0.4 0 -0.7 0.3 -0.7 0.6v1.9c0 0.3 0.3 0.6 "
    "0.6 0.6h0.2c0 0 0 0.1 0 0.1v1.9c0 0.3 0.2 0.6 0.3 "
    "0.6h1.3c0.2 0 0.3 -0.3 0.3 -0.6v-1.8c0 0 0 -0.1 0 "
    "-0.1h0.2c0.3 0 0.6 -0.3 0.6 -0.6v-2c0.2 -0.3 -0.1 "
    "-0.6 -0.4 -0.6z"
)

chart = alt.Chart(graphdata).transform_calculate(
    row="ceil(datum.id/10)"
).transform_calculate(
    col="datum.id - datum.row*10"
).mark_point(
    filled=True,
    size=80
).encode(
    x=alt.X("col:O", axis=None),
    y=alt.Y("row:O", axis=None),
    shape=alt.ShapeValue(person),
    color=alt.Color("Prediction Result", legend=None).scale(domain=["Correct Recidivism", "Wrong Recidivism", "Correct Non-Recidivism", "Wrong Non-Recidivism"], range=["red", "black", "blue", "purple"])
).properties(
    width=400,
    height=400
).configure_view(
    strokeWidth=0
)
    
st.altair_chart(chart)