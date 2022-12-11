import streamlit as st

import pandas as pd
from sklearn.neighbors import NearestNeighbors
import plotly.express as px
import streamlit.components.v1 as components
from PIL import Image

# Check if 'key' already exists in session_state
# If not, then initialize it
if "key" not in st.session_state:
    st.session_state["key"] = "value"

st.set_page_config(
    page_title="CSCI-4220",
    page_icon="💯",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
        "Get help": "https://gitlab.com/briceallen/csci-4220.git",
        "Report a bug": "https://gitlab.com/briceallen/csci-4220.git",
        "About": "# *Extemely* cool app!",
    },
)


# # Cache expensive data read
@st.cache(allow_output_mutation=True, suppress_st_warning=True)
def load_data():
    # Displays on first run while loading data.
    st.write("CACHE MISS: Successfully loaded data into cache.")
    df = pd.read_csv("data/cleaned_data.csv")
    df["genres"] = df.genres.apply(
        lambda x: [i[1:-1] for i in str(x)[1:-1].split(", ")]
    )
    exploded_track_df = df.explode("genres")
    return exploded_track_df


g = [
    "Pop",
    "Electronic",
    "Hip Hop",
    "Jazz",
    "Rap",
    "Jazz Rap",
    "Metal",
    "Wolrd",
    "Rock",
]
audio_feats = [
    "acousticness",
    "danceability",
    "energy",
    "instrumentalness",
    "valence",
    "tempo",

]

track_df = load_data()


def kth_neighbor(g, begin, end, cats):
    df = track_df[
        (track_df["genres"] == g.lower())
        & (track_df["release_year"] >= begin)
        & (track_df["release_year"] <= end)
        ]
    df = df.sort_values(by="popularity", ascending=False)[:1000]
    neigh = NearestNeighbors()
    neigh.fit(df[audio_feats].to_numpy())
    n_neighbors = neigh.kneighbors(
        [cats], n_neighbors=len(df), return_distance=False
    )[0]
    ids = df.iloc[n_neighbors]["uri"].tolist()
    cats = df.iloc[n_neighbors][audio_feats].to_numpy()
    return ids, cats


st.write("""# CSCI-4220""")
st.write("""## Explanation:""")
st.write(
    "Select which Genre you prefer on the left. Play around with the sliders "
    "too. The recommendations are generated using the K-Nearest Neighbors "
    "model. "
)

# image
image = Image.open("img/namroud-gorguis-FZWivbri0Xk-unsplash.jpg")
st.image(image)

# Bring in the data
st.write("## THE DATA BEING USED")
track_df
st.markdown("# ")
st.markdown("# ")
genre = st.sidebar.radio('GENRE', g, index=g.index("Jazz"))
st.markdown("# ")
st.markdown("# ")
with st.container():
    [left, mid, right] = st.columns([3, 0.5, 0.5])
    with left:
        st.markdown("## SLIDERS")
        begin, end = st.slider("Year", 1950, 2022, (1955, 1999))
        ac = st.slider("Acousticness", 0.0, 1.0, 0.5)
        d = st.slider("Danceability", 0.0, 1.0, 0.5)
        e = st.slider("Energy", 0.0, 1.0, 0.5)
        inst = st.slider("Instrumentalness", 0.0, 1.0, 0.0)
        v = st.slider("Valence", 0.0, 1.0, 0.5)
        t = st.slider("Tempo", 0.0, 240.0, 100.0)

categories = [ac, d, e, inst, v, t]
ids, audioo = kth_neighbor(genre, begin, end, categories)
pagination = 8
tracks = []
for uri in ids:
    track = """<iframe src="https://open.spotify.com/embed/track/{}"
    width="260" height="380" frameborder="0" allowtransparency="true"
    allow="encrypted-media"></iframe>""".format(uri)
    tracks.append(track)

if "previous_inputs" not in st.session_state:
    st.session_state["previous_inputs"] = [genre, begin, end] + categories

current = [genre, begin, end] + categories
if current != st.session_state["previous_inputs"]:
    if "start_track_i" in st.session_state:
        st.session_state["start_track_i"] = 0
    st.session_state["previous_inputs"] = current

if "start_track_i" not in st.session_state:
    st.session_state["start_track_i"] = 0

with st.container():
    [left, mid, right] = st.columns([3, 1.5, 3])
    if st.button("Next Page") and st.session_state[
        "start_track_i"
    ] < len(tracks):
        st.session_state["start_track_i"] += pagination

    audio_state = audioo[
                  st.session_state["start_track_i"]: st.session_state[
                                                         "start_track_i"]
                                                     + pagination
                  ]

    track_state = tracks[
                  st.session_state["start_track_i"]: st.session_state[
                                                         "start_track_i"]
                                                     + pagination
                  ]

    if st.session_state["start_track_i"] < len(tracks):
        for i, (track, audio) in enumerate(zip(track_state, audio_state)):
            if i & 1 == 0:
                with left:
                    components.html(
                        track,
                        height=400,
                    )
                    with st.expander("Graph: "):
                        df = pd.DataFrame(
                            dict(r=audio[:5], theta=audio_feats[:5]))
                        fig = px.line_polar(
                            df, r="r", theta="theta", line_close=True,
                            direction="counterclockwise", start_angle=45,
                            title="Song"
                        )
                        fig.update_traces(fill='toself')
                        fig.update_layout(height=400, width=400)
                        st.plotly_chart(fig)

            else:
                with right:
                    components.html(
                        track,
                        height=400,
                    )
                    with st.expander("Graph:"):
                        df = pd.DataFrame(
                            dict(r=audio[:5], theta=audio_feats[:5]))
                        fig = px.line_polar(
                            df, r="r", theta="theta", line_close=True,
                            direction="counterclockwise", start_angle=45
                        )
                        fig.update_traces(fill='toself')
                        fig.update_layout(height=400, width=400)
                        st.plotly_chart(fig)

    else:
        st.write("The END.")
