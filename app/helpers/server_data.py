from app.models import Tramo, TipoCombustible, PuntoControl, \
    ClasificacionControl, ResponsableControl, Laboratorista, Region, TipoRed


def create_region(db):
    regiones = [
        [1, 'Arica y Parinacota'],
        [2, 'Tarapacá'],
        [3, 'Antofagasta'],
        [4, 'Atacama'],
        [5, 'Coquimbo'],
        [6, 'Valparaiso'],
        [7, 'Metropolitana de Santiago'],
        [8, 'Libertador General Bernardo O\'Higgins'],
        [9, 'Maule'],
        [10, 'Biobío'],
        [11, 'La Araucanía'],
        [12, 'Los Ríos'],
        [13, 'Los Lagos'],
        [14, 'Aisén del General Carlos Ibáñez del Campo'],
        [15, 'Magallanes y de la Antártica Chilena'],
        [16, 'No Aplica']
    ]
    for region in regiones:
        new_region = Region(
            id=region[0],
            name=region[1]
        )
        db.session.add(new_region)
        db.session.commit()


def create_tramo(db):
    tramos = [
        [1, 'No Aplica'],
        [2, 'Calama'],
        [3, 'Caletones'],
        [4, 'Chillan'],
        [5, 'Colmo'],
        [6, 'Concepcion'],
        [7, 'Escobares'],
        [8, 'Los Angeles'],
        [9, 'Lo Venecia'],
        [10, 'Porvenir'],
        [11, 'Puerto Natales'],
        [12, 'Punta Arenas'],
        [13, 'Rancagua'],
        [14, 'Santiago'],
        [15, 'Tapihue'],
        [16, 'Temuco'],
        [17, 'Osorno'],
        [18, 'Porvenir']
    ]

    for tramo in tramos:
        new_tramo = Tramo(
            id=tramo[0],
            name=tramo[1]
        )
        db.session.add(new_tramo)
        db.session.commit()


def create_tipo_red(db):
    tipos = [
        [1, "PSRI"],
        [2, "RED"],
        [3, "REDBM"],
        [4, "PSR"]
    ]

    for tipo in tipos:
        new_tipo_red = TipoRed(
            id=tipo[0],
            name=tipo[1]
        )
        db.session.add(new_tipo_red)
        db.session.commit()


def create_punto_control(db):
    puntos_control = [
        ['PSR CHOROMBO', "Punto de Control Pta.Regasificación Chorombo", 1, 7, 1],
        ['PSR EL PAICO', "Punto de Control Pta.Regasificación El Paico", 1, 7, 1],
        ['PSR FRUTEXSA', "Punto de Control Pta.Regasificación Frutexsa", 1, 7, 1],
        ['PSR IANSA', "Punto de Control Pta.Regasificación Iansa", 1, 7, 1],
        ['PSR NUTRICION', "Punto de Control Pta.Regasificación Nutrición", 1, 7, 1],
        ['PSR RENDERING', "Punto de Control Pta.Regasificación Rendering", 1, 7, 1],
        ['PSR SANTA ROSA', "Punto de Control Pta.Regasificación Santa Rosa", 1, 7, 1],
        ['PSR ALIMENTOS', "Punto de Control Pta.Regasificación Alimentos", 1, 7, 1],
        ["CG1", "Punto de Control City Gate  1", 2, 7, 14],
        ["CG2", "Punto de Control City Gate  2", 2, 7, 14],
        ["CG3", "Punto de Control City Gate  3", 2, 7, 14],
        ["DANIEL GC2", "Punto de Control City Gate  2 Cromatografo Daniels", 2, 7, 14],
        ["DANIEL MAIPÚ", "Punto de Control Maipu Cromatografo Daniels", 2, 7, 14],
        ["ELECTROGAS CG3", "Cromatografo CG3 Electrogas", 2, 7, 14],
        ["ERP 11", "Punto de Control Estación Regulación 11", 2, 7, 14],
        ["ERP 1A", "Punto de Control Estación Regulación 1-A", 2, 7, 14],
        ["ERP 1C-1", "Punto de Control Estación Regulación 1C-1", 2, 7, 14],
        ["ERP 21A", "Punto de Control Estación Regulación 21-A", 2, 7, 14],
        ["ERP 29", "Punto de Control Estación Regulación 29", 2, 7, 14],
        ["ERP 32-2", "Punto de Control Estación Regulación 32-2", 2, 7, 14],
        ["ERP 3B-2", "Punto de Control Estación Regulación 3B-2", 2, 7, 14],
        ["ERP 3B-3", "Punto de Control Estación Regulación 3B-3", 2, 7, 14],
        ["ERP38", "Punto de Control Estación Regulación 38", 2, 7, 14],
        ["ERP39", "Punto de Control Estación Regulación 39", 2, 7, 14],
        ["LA FARFANA", "Punto de Control Planta Biometano La Farfana", 2, 7, 14],
        ["MEZCLA P1", "Punto de Control ingreso Biometano Pto.1", 3, 7, 14],
        ["MEZCLA P2", "Punto de Control ingreso Biometano Pto.2", 3, 7, 14],
        ["MEZCLA P3", "Punto de Control ingreso Biometano Pto.3", 3, 7, 14],
        ["MEZCLA P4", "Punto de Control ingreso Biometano Pto.4", 3, 7, 14],
        ["MEZCLA P5", "Punto de Control ingreso Biometano Pto.5", 3, 7, 14],
        ["PSR CORONEL Punto de Control", "Pta. Regasificación Coronel", 1, 10, 1],
        ["PSR LOS ANGELES", "Punto de Control Pta. Regasificación Los Angeles", 1, 10, 1],
        ["PSR CCU TEMUCO", "Punto de Control Pta. Regasificación PSR CCU Temuco", 1, 11, 1],
        ["PSR SAN FERNANDO CARTONES", "Punto de Control Pta. Regasificación San Fernando Cartones", 1, 8, 1],
        ["PSR SAN FERNANDO NESTLE", "Punto de Control Pta. Regasificación San Fernando Nestle", 1, 8, 1],
        ["ERP 134-A", "Punto de Control Estacion Regulacion 134-A(Rancagua)", 2, 8, 13],
        ["ERP 136", "Punto de Control Estacion Regulacion 136", 2, 8, 13],
        ["LA CANDELARIA", "Punto de Control La Candelaria", 2, 8, 13],
        ["PSR OSORNO RESIDENCIAL", "Punto de Control PSR Residencial Osorno", 4, 13, 17],
        ["PSR CANCURA", "Punto de Control pta Regasificacion Cancura", 1, 13, 1],
        ["PSR LLANQUIHUE", "Punto de control Pta. Regasificacion LLanquihue", 1, 13, 1],
        ["PSR LA UNION", "Punto de control Pta. Regasificacion La Union", 1, 12, 1]
    ]
    for punto_control in puntos_control:
        new_punto_control = PuntoControl(
            name=punto_control[0],
            descripcion=punto_control[1],
            tipo_red_id=punto_control[2],
            region_id=punto_control[3],
            tramo_id=punto_control[4]
        )
        db.session.add(new_punto_control)
        db.session.commit()


def create_tipo_combustible(db):
    combustibles = [
        [1, 'Mezcla GN/BM'],
        [2, 'Aire Metanado'],
        [3, 'Aire Propanado'],
        [4, 'Biometano'],
        [5, 'Gas de Ciudad'],
        [6, 'Gas Natural']
    ]

    for combustible in combustibles:
        new_combustible = TipoCombustible(
            id=combustible[0],
            name=combustible[1]
        )
        db.session.add(new_combustible)
        db.session.commit()


def create_clasificacion_control(db):
    clasificaciones = [
        [1, 'Analisis Laboratorio'],
        [2, 'Cromatografia'],
        [3, 'Cromatografia y Otros'],
        [4, 'Punto de Control de Red'],
        [5, 'Punto de Odorizacion en Red']
    ]

    for clasificacion in clasificaciones:
        new_clasificacion = ClasificacionControl(
            id=clasificacion[0],
            name=clasificacion[1]
        )
        db.session.add(new_clasificacion)
        db.session.commit()


def create_responsable_control(db):
    responsables = [
        [1, 'Propio'],
        [2, 'Proovedor'],
        [3, 'Transportista']
    ]

    for responsable in responsables:
        new_responsable = ResponsableControl(
            id=responsable[0],
            name=responsable[1]
        )
        db.session.add(new_responsable)
        db.session.commit()


def create_laboratorista(db):
    laboratoristas = [
        [1, 'Nataly Plaza'],
        [2, 'Lisette Aravena'],
        [3, 'Jose Barrera'],
        [4, 'Marco Acevedo']
    ]
    for laboratorista in laboratoristas:
        new_laboratorista = Laboratorista(
            id=laboratorista[0],
            name=laboratorista[1]
        )
        db.session.add(new_laboratorista)
        db.session.commit()
