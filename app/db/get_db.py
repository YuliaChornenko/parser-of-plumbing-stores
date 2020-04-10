from pymongo import MongoClient
import pandas as pd


client = MongoClient('mongodb://romasoya1402:Roma1989Soya@cluster0-shard-00-00-zkewx.mongodb.net:27017,cluster0-shard-00-01-zkewx.mongodb.net:27017,cluster0-shard-00-02-zkewx.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority')
db = client.b2b
agromat_cat =['A.L.F. UNO', 'ABK', 'ABSOLUT KERAMIKA', 'ACF', 'ACO', 'ALMERA CERAMICA (SPAIN)', 'ALMERA CERAMICA-2', 'AM.PM', 'ANTONIO LUPI', 'APARICI', 'APE Ceramica', 'ASCOT', 'AXO', 'AZTECA', 'AZUVI', 'Alaplana', 'Alberta Salotti', 'Alfobel', 'Alt Lucialternative', 'Altrenotti', 'Antealuce', 'Appollo', 'Argenta Ceramica', 'Ariana', 'Arizzi', 'Arteflash', 'Atis', 'Aureliano Toso', 'Axor', 'Azulev', 'B Belle Italia', 'BADARI', 'BALDOCER', 'BESTILE', 'BETTER-мозаика', 'BRAVAT', 'BUTECH', 'Bagno associati', 'Balteco', 'Barovier&Toso', 'Baumit', 'BellArt', 'Bellavista Ceramica', 'Bette', 'Blanco', 'Bongio', 'Bossini', 'Botticelli', 'Burg', 'CAESAR', 'CERACASA', 'CERAM GOMEZ', 'CERAMICA DESEO', 'CERRAD', 'CERROL', 'CIELO', 'CIR', 'CISAL', 'CLASSIC LIGHT - VOLTOLINA', 'COLLI CERAMICA', 'COLOMBO', 'CRISTACER', 'CTF srl.', 'Ceramica Gomez', 'Ceramica de LUX', 'Ceranosa', 'Ceresit', 'Cersanit', 'Cicogres', 'Creazioni', 'DECOR MARMI', 'DEVIT', 'DIETSCHE', 'DOMI S.r.l.', 'DORNBRACHT', 'DURAVIT', 'Damixa', 'Del Conca', 'Ditre Italia s.r.l', 'Dorelan', 'Draenert', 'Dual Gres', 'Duscholux', 'EGOLUCE', 'EMCO', 'EMIL CERAMICA', 'ESEDRA', 'EXAGRES', 'Eichholtz', 'Electrolux', 'F.B.A.I.', 'FABBIAN', 'FAUSTIG', 'FERRO', 'FLAMINIA', 'FLAVIKER', 'FLORIM GROUP', 'FONDOVALLE', 'Fabresa', 'Felis', 'Fine ArtLamp', 'Franke', 'GAMBARELLI', 'GBGroup', 'GENOVEVA', 'GENWEC', 'GEOTILES', 'GESSI', 'GOLDEN TILE', 'GRAND KERAMA', 'GRESMANC', 'Gallo', 'Geberit', 'Gemma', 'Gentry Home', 'Giorgio Casa', 'Giovanetti Collezioni', 'Giusti Portos', 'Goldencer', 'Goldman', 'Gorenje', 'Gresan', 'Grohe', 'Gustavsberg', 'HALCON', 'HARDEX', 'HUPPE', 'Hansgrohe', 'I4 MARIANI', 'IBERO', 'IDO', 'ILLUMINAZIONE', 'IMOLA', 'IMSO CERAMICA', 'INSTAL PROJEKT', 'INTERSTYLE', 'IRIS', 'ITALAMP', 'ITALGRANITI', 'ITRE', 'ITT CERAMIC', 'Ideal Standard', 'Ilfari', 'Illuminati', 'Impronta', 'JAB furniture', 'JACUZZI', 'JIKA', 'Jacob Delafon', 'Jago', 'KERAMAG', 'KITO', 'KOLO', 'KOS', 'KUNDALINI', 'Kaldewei', 'Karman', 'Keraben', 'Keramo Rosso', 'Kerasan', 'Keratile', 'Kludi', 'Knauf', 'Koinor', "L'Antic Colonial", "L'Originale", 'LA FABBRICA', 'LA FAENZA', 'LAMPADARI', 'LAND PORCELANICO', 'LAUFEN', 'LEONARDO', 'LEUCOS', 'LINEALIGHT', 'LIVIN CERAMICS', 'LLADRO', 'LOVE CERAMIC', 'La Ebanisteria', 'La Platera', 'Labor Legno', 'Lamp International', 'Langberger', 'Lasselsberger Rako', 'Liberta', 'Litokol', 'MAINZU', 'MAPISA', 'MARCA CORONA', 'MARCHETTI', 'MARGAROLI', 'MARINER', 'MASCA', 'MASIERO', 'MAYOLICA', 'MEGAGRES', 'MEGAGRES-2', 'METALSPOT', 'MIDJ', 'MIRA', 'MIRAGE', 'MO.WA.', 'MONOPOLE CERAMICA', 'MONTEVECCHIA', 'MOZAICO DE LUX', 'Malerba S.R.L', 'Mapei', 'Mario', 'Maritima', 'Moscatelli', 'Myyour', 'NATUCER', 'NIC Design', 'NOKEN', 'NOVABELL', 'NOVOGRES', 'NOWA GALA', 'NerviLamp', 'Newker', 'Nicoll', 'Nurhas Mobilya', 'OLIVEIRA', 'OPOCZNO PL', 'OPOCZNO PL+', 'OPOCZNO UA', 'ORAS', 'OSET', 'OVERLAND', 'Oceano', 'P&Vlighting', 'PAA', 'PAMESA', 'PANZERI', 'PATAVIUMART', 'PATRIZIAGARGANTI - BAGA', 'PEOPLE&LIGHT', 'PERONDA', 'PIEMME CERAMICHE', 'POSSONI', 'PREARO', 'PREARO-мебель', 'PRIMERA', 'PROGRESS PROFILE', 'Paffoni', 'Pax', 'Porcelanite Dos', 'Porta', 'Presotto', 'Prevex AB', 'Prissmacer', 'RAK Ceramics Sanitaryware', 'REALONDA', 'REVIGRES', 'RICCHETTI CERAMICHE', 'RIHO', 'ROBERTO CAVALLI', 'RONDINE', 'ROYO', 'Rocersa', 'Rozzoni Mobili', 'SALONI', 'SANIT', 'SDS KERAMIK', 'SERENISSIMA', 'SERENISSIMA - МЕБЕЛЬ', 'SETTECENTO', 'SIGNORINI-COCO', 'SIMAS', 'SLIDE', 'SMA Mobili Spa', 'SUEGNO', 'Salgar', 'San Swiss', 'Sanchis', "Seduta D' Arte", 'Simand', 'Sitap', 'Smavit', 'Soler&Palau', 'Sopro', 'Status', 'Steinberg', 'Steinpol', 'Stella di Mare', 'Still-Lux', 'Stoner', 'Styron', 'Super Ceramica', 'TAU', 'TERMAL SERAMIK', 'TODAGRES', 'TONIN CASA', 'TREESSE', 'Targetti', 'Tece', 'Terma', 'Terranit', 'Thermex', 'Topwell Stone', 'Tosconova srl.', 'Unicom Starker', 'VAGNERPLAST', 'VALENTI', 'VALLELUNGA', 'VENIS', 'VIBIA', 'VICTORIA', 'VISO', 'VITRABLOK', 'VIVES', 'Valmori', 'Venus', 'Viega', 'Villeroy&Boch', 'Voglauer', 'WGT', 'WIM', 'ZONCA', 'ZUCCHETTI', 'Zanussi', 'Zehnder', 'Zeus Ceramica', 'de Majo', 'АТЕМ', 'Агромат-Декор', 'Аква Родос', 'Берёзакерамика', 'Бусел', 'Вист', 'КІП КЕРАМІКА', 'Керамика Полесье', 'Мастерская Зеркал', 'Полипласт', 'Разові поставки', 'Разові поставки Україна', 'ТОВ "MCH ІНЖИНІРИНГ"', 'ТОВ "КРИМАРТ"', 'Ювента']




def connection(table_name):
    client = MongoClient('mongodb://romasoya1402:Roma1989Soya@cluster0-shard-00-00-zkewx.mongodb.net:27017,cluster0-shard-00-01-zkewx.mongodb.net:27017,cluster0-shard-00-02-zkewx.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority')
    db = client.b2b
    table = db[table_name].find()

    return table


def prepare_csv(table_name):
    docs = pd.DataFrame(list(connection(table_name)))
    string = 'app/db/data/' + str(table_name) + '.csv'
    docs = docs.to_csv(string, index = False)



# table = connection('sandi_db')
# docs = pd.DataFrame(list(connection('sandi_db')))
# docs.to_excel('data/test.xlsx',index=None, header=True)
