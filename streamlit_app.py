import streamlit as st

def prikazi_pitanje(index, pitanje, odgovori, tocni_odgovor):
    st.subheader(f"Pitanje {index + 1}: {pitanje}")
    izbor = st.radio("Odaberite odgovor:", odgovori, index=None, key=index)
    if st.button("Potvrdi", key=f"btn_{index}"):
        if izbor == tocni_odgovor:
            st.success("✔ Točno! Idemo dalje.")
            return True
        else:
            st.error("✖ Netočno. Pokušajte ponovno.")
    return False

def simulacija():
    st.title("Simulacija Operatera")
    st.write("Odgovorite na pitanja kako biste prošli kroz scenarije.")
    
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
    
    bodovi = 0
    for index, scenarij in enumerate(scenariji):
        if prikazi_pitanje(index, scenarij["pitanje"], scenarij["odgovori"], scenarij["tocni"]):
            bodovi += 1
    
    st.write(f"**Simulacija završena! Osvojili ste {bodovi}/{len(scenariji)} bodova.**")

if __name__ == "__main__":
    simulacija()
