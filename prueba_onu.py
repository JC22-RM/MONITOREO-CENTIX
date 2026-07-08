from smartolt import obtener_onus

onus = obtener_onus()

print("TOTAL ONUS:", len(onus))

if len(onus) > 0:
    print("PRIMER CLIENTE:")
    print(onus[0])