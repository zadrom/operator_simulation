import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from io import BytesIO
import time

def kreiraj_shemu():
    g = nx.Graph()
    tstations = {
        "TS1": "brown", "TS2": "darkblue", "TS01": "brown", "TS02": "brown", "TS03": "brown", "TS04": "brown", 
        "TS05": "brown", "TS06": "darkblue", "TS07": "darkblue", "TS08": "darkblue", "TS09": "darkblue"
    }
    g.add_nodes_from(tstations.keys())
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
    edge_colors = [edges.get(edge, "lightblue") for edge in g.edges]
    pos = {
        "TS1": (-3, 2), "TS2": (3, 2),
        "TS01": (-2, 1), "TS02": (0, 1), "TS03": (2, 1),
        "TS04": (-2, 0), "TS05": (0, 0), "TS06": (2, 0),
        "TS07": (-2, -1), "TS08": (0, -1), "TS09": (2, -1)
    }
    fig, ax = plt.subplots(figsize=(10, 6))
    nx.draw(g, pos, with_labels=True, node_size=3000, 
            node_color=[tstations[node] for node in g.nodes()], 
            edge_color=edge_colors, font_size=12, font_weight='bold', ax=ax)
    nx.draw_networkx_edge_labels(g, pos, edge_labels=edge_labels, font_size=10, font_color='red', ax=ax)
    ax.set_title("Shema elektrodistribucijske mreže")
    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    return buf

def prikazi_pitanje(pitanje, odgovori, tocni_odgovor):
    st.image(kreiraj_shemu())
    st.write("### " + pitanje)
    izbor = st.radio("Odaberite točan odgovor:", odgovori)
    if st.button("Potvrdi odgovor", key=f"button_{pitanje}"):
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
        time.sleep(1)
    st.write(f"## Simulacija završena! Osvojili ste {bodovi}/{len(scenariji)} bodova.")

if __name__ == "__main__":
    st.title("Simulacija Operatora Elektrodistribucije")
    simulacija()
