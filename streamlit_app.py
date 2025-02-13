import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx

# Funkcija za crtanje mreže
def nacrtaj_mrezu():
    g = nx.Graph()
    
   # Dodavanje trafostanica
tstations = {
    "TS1": "brown", "TS2": "darkblue", "TS01": "brown", "TS02": "brown", "TS03": "brown", "TS04": "brown", 
    "TS05": "brown", "TS06": "darkblue", "TS07": "darkblue", "TS08": "darkblue", "TS09": "darkblue"
}
    # Povezivanje dalekovodima
    edges = {
    ("TS1", "TS01"): "green", ("TS01", "TS02"): "green", ("TS02", "TS03"): "green", ("TS03", "TS2"): "lightblue", 
    ("TS1", "TS04"): "green", ("TS04", "TS05"): "green", ("TS05", "TS06"): "lightblue", ("TS2", "TS06"): "green", 
    ("TS1", "TS07"): "lightblue", ("TS2", "TS09"): "green", ("TS08", "TS09"): "green", ("TS07", "TS08"): "green", 
    ("TS04", "TS02"): "lightblue", ("TS05", "TS09"): "lightblue"
}
edge_labels = {
    ("TS1", "TS01"): "D1", ("TS01", "TS02"): "D2", ("TS02", "TS03"): "D3", ("TS03", "TS2"): "D4", 
    ("TS1", "TS04"): "D5", ("TS04", "TS05"): "D6", ("TS05", "TS06"): "D7", ("TS06", "TS2"): "D8", 
    ("TS1", "TS07"): "D9", ("TS2", "TS09"): "D12", ("TS09", "TS08"): "D11", ("TS08", "TS07"): "D10", 
    ("TS04", "TS02"): "D13", ("TS05", "TS09"): "D14"
}
g.add_edges_from(edges.keys())

# Osiguravanje da svi rubovi imaju definisane boje
edge_colors = [edges.get(edge, "lightblue") for edge in g.edges]

# Prilagođavanje pozicija kako bi se izbjeglo preklapanje vodova
pos = {
    "TS1": (-3, 2), "TS2": (3, 2),
    "TS01": (-2, 1), "TS02": (0, 1), "TS03": (2, 1),
    "TS04": (-2, 0), "TS05": (0, 0), "TS06": (2, 0),
    "TS07": (-2, -1), "TS08": (0, -1), "TS09": (2, -1)
}  
    g.add_edges_from(tstations.keys())
    
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

