import streamlit as st
import plotly.graph_objects as go
import networkx as nx

# Funkcija za crtanje mreže
def nacrtaj_mrezu():
    g = nx.Graph()
    
    # Čvorovi (trafostanice)
    g.add_nodes_from(["TS1", "TS2", "TS01", "TS02", "TS03", "TS04", "TS05", "TS06", "TS07", "TS08", "TS09"])
    
    # Povezivanje dalekovodima
    edges = [("TS1", "TS01"), ("TS01", "TS02"), ("TS02", "TS03"), ("TS03", "TS2"),
             ("TS1", "TS04"), ("TS04", "TS05"), ("TS05", "TS06"), ("TS06", "TS2"),
             ("TS2", "TS09"), ("TS09", "TS08"), ("TS08", "TS07")]
    
    g.add_edges_from(edges)
    
    # Crtanje mreže
    pos = nx.spring_layout(g)
    fig, ax = plt.subplots(figsize=(6, 4))
    nx.draw(g, pos, with_labels=True, node_color='lightblue', edge_color='green', node_size=2000, font_size=10, ax=ax)
    
    return fig

# Prikaz sheme na vrhu aplikacije
st.header("Shema elektrodistribucijske mreže")
fig = nacrtaj_mrezu()
st.pyplot(fig)
st.divider()  # Razdvajanje pitanja od sheme

# Lista scenarija
scenariji = [
    {"pitanje": "Kvar na dalekovodu D3. Kako osigurati napajanje?",
     "odgovori": ["Prebaciti opterećenje na D1 i D2", "Isključiti TS1", "Uključiti D4", "Povezati D5 i D6", "Ne poduzimati ništa"],
     "tocni": "Uključiti D4"},
    
    {"pitanje": "Planirani radovi na TS05. Što učiniti prvo?",
     "odgovori": ["Odmah isključiti TS05", "Obavijestiti korisnike i osigurati alternativno napajanje", "Ignorirati", "Isključiti cijelu mrežu", "Pojačati napon na TS04"],
     "tocni": "Obavijestiti korisnike i osigurati alternativno napajanje"},
    
    {"pitanje": "Neočekivano preopterećenje na dalekovodu D8. Koji je ispravan postupak?",
     "odgovori": ["Povećati opterećenje na D9", "Izolirati D8 i preusmjeriti teret", "Isključiti cijelu mrežu", "Isključiti TS09", "Ne poduzimati ništa"],
     "tocni": "Izolirati D8 i preusmjeriti teret"},
    
    {"pitanje": "TS2 ostaje bez napajanja. Što učiniti?",
     "odgovori": ["Preusmjeriti napajanje s TS1", "Isključiti sve trafostanice", "Povećati napon na D12", "Povezati TS2 direktno na D7", "Ne poduzimati ništa"],
     "tocni": "Preusmjeriti napajanje s TS1"}
]

# Inicijalizacija stanja korisnika
if "index" not in st.session_state:
    st.session_state.index = 0
if "bodovi" not in st.session_state:
    st.session_state.bodovi = 0

# Placeholder za dinamičko prikazivanje pitanja
placeholder = st.empty()

if st.session_state.index < len(scenariji):
    scenarij = scenariji[st.session_state.index]
    
    with placeholder.container():
        st.subheader(scenarij["pitanje"])
        izbor = st.selectbox("Odaberite točan odgovor:", scenarij["odgovori"], key=st.session_state.index)
        
        if st.button("Potvrdi"):
            if izbor == scenarij["tocni"]:
                st.success("✔ Točno! Idemo dalje.")
                st.session_state.bodovi += 1
            else:
                st.error("✖ Netočno. Pokušajte ponovno.")

            # Prelazak na sljedeće pitanje
            st.session_state.index += 1
            st.experimental_rerun()
else:
    # Završna poruka
    st.success(f"Simulacija završena! Osvojili ste {st.session_state.bodovi}/{len(scenariji)} bodova.")
    st.balloons()
