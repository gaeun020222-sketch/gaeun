import streamlit as st
import pandas as pd
import numpy as np
st.title('My First Streamlit App')
st. write("Here's our first attempt at using data to create a table:")
st.write(pd.DataFrame({
    'first column':[1, 2, 3,4],
    'second column':[10, 20, 30, 40]
}))

import streamlit as st
import pandas as pd
import numpy as np

st.write("Streamlit supports a wide range of data visualizations, including Plotly, Altair, and Bokeh charts.")

all_users = ["Alice", "Bob", "Charly"]
with st.container(border=True):
    users = st.multiselect("Users", all_users, default=all_users)
    rolling_average = st.toggle("Rolling average")

np.random.seed(42)
data = pd.DataFrame(np.random.randn(20, len(users)), columns=users)
if rolling_average:
    data = data.rolling(7).mean().dropna()

tab1, tab2 = st.tabs(["Chart", "Dataframe"])
tab1.line_chart(data, height=250)
tab2.dataframe(data, height=250, use_container_width=True)



import streamlit as st
import pandas as pd
import numpy as np

st.write("Got lots of data? Great! Streamlit can show [dataframs] with hundred thousands of rows, images, sparklines-and even supports editing!")

num_rows = st.slider("Number of rows", 1, 1000, 500)
np. random.seed(42)
data = []
for i in tange(num_rows):
    data.append(
        {
            "Preview": f"http://picsum.photos/400/200?lock={i}",
            "Views": np.random.randint(0, 100),
            "Active": np.random.choice([True, False]),
            "Category": np.ramdom.choice(["LLM", "Data", "Tool"])
            "Progress": np.random.randiant(1, 100),
        }
    )
data = pd.DataFrame(data)

config = {
    "Preview": st.column_config.ImageColimn(),
    "Progress": st.column_config.ProgressColumn(),
}

if st.toggle("Enable editing"):
    edited_data = st.data_editor(data, column_config=config, use_container_width=True)
else:
    st.dataframe(data, column_config=config, use_container_width=True)
