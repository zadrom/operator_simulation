import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx

def prikazi_shemu():
    G = nx.Graph()
    
    # Definicija trafostanica i njihovih položaja
    pos = {
        "TS1": (0, 3), "TS2": (8, 3),
        "TS01": (2, 3), "TS02": (4, 3), "TS03": (6, 3),
        "TS04": (2, 2), "TS05": (4, 2), "TS06": (6, 2),
        "TS07": (2, 1), "TS08": (4, 1), "TS09": (6, 1)
    }
    
    # Definicija dalekovoda
    edges = {
        ("TS1", "TS01"): "D1", ("TS01", "TS02"): "D2", ("TS02", "TS03"): "D3", ("TS03", "TS2"): "D4",
        ("TS1", "TS04"): "D5", ("TS04", "TS05"): "D6", ("TS05", "TS06"): "D7", ("TS06", "TS2"): "D8",
        ("TS1", "TS07"): "D9", ("TS07", "TS08"): "D10", ("TS08", "TS09"): "D11", ("TS09", "TS2"): "D12"
    }
    
    # Dodavanje čvorova i grana u graf
    G.add_edges_from(edges.keys())
    
    # Definicija boja trafostanica prema napojnoj točki
    node_colors = {
        "TS1": "red", "TS2": "blue",
        "TS01": "red", "TS02": "red", "TS03": "blue",
        "TS04": "red", "TS05": "red", "TS06": "blue",
        "TS07": "red", "TS08": "blue", "TS09": "blue"
    }
    
    # Definicija boja dalekovoda
    edge_colors = {edge: "green" for edge in edges}  # Svi dalekovodi su aktivni na početku
    
    fig, ax = plt.subplots()
    nx.draw(G, pos, with_labels=True, node_color=[node_colors[node] for node in G.nodes],
            edge_color=[edge_colors[edge] for edge in G.edges], font_weight='bold', ax=ax)
    
    # Dodavanje oznaka dalekovoda
    edge_labels = {edge: name for edge, name in edges.items()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='black', ax=ax)
    
    st.pyplot(fig)

st.title("Simulacija elektrodistribucijske mreže")
prikazi_shemu()

def prikazi_pitanje(pitanje, odgovori, tocni_odgovor):
    izbor = st.radio(pitanje, odgovori)
    if st.button("Potvrdi odabir"):
        if izbor == tocni_odgovor:
            st.success("✔ Točno! Idemo dalje.")
            return True
        else:
            st.error("✖ Netočno. Pokušajte ponovno.")
    return False

def simulacija():
    bodovi = 0
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
    
    for scenarij in scenariji:
        if prikazi_pitanje(scenarij["pitanje"], scenarij["odgovori"], scenarij["tocni"]):
            bodovi += 1
    
    st.write(f"\nSimulacija završena! Osvojili ste {bodovi}/{len(scenariji)} bodova.")

simulacija()


