from settings import MEREK_SCALE,DEV_SCALE_processor,DEV_SCALE_ram,DEV_SCALE_storage,DEV_SCALE_baterai,DEV_SCALE_harga

class BaseMethod():

    def __init__(self, data_dict, **setWeight):

        self.dataDict = data_dict

        # 1-7 (Kriteria)
        self.raw_weight = {
            'Merk': 5, 
            'Processor': 3, 
            'Memori_Internal': 4, 
            'RAM': 3, 
            'Baterai': 4, 
            'Harga': 3, 
        }

        if setWeight:
            for item in setWeight.items():
                temp1 = setWeight[item[0]] # value int
                temp2 = {v: k for k, v in setWeight.items()}[item[1]] # key str

                setWeight[item[0]] = item[1]
                setWeight[temp2] = temp1

    @property
    def weight(self):
        total_weight = sum(self.raw_weight.values())
        return {c: round(w/total_weight, 2) for c,w in self.raw_weight.items()}

    @property
    def data(self):
        return [{
            'id': laptop['id'],
            'Merk': MEREK_SCALE[laptop['Merk']],
            'Processor': DEV_SCALE_processor[laptop['Processor']],
            'Memori_Internal': DEV_SCALE_storage[laptop['Memori_Internal']],
            'RAM': DEV_SCALE_ram[laptop['RAM']],
            'Baterai': DEV_SCALE_baterai[laptop['Baterai']],
            'Harga': DEV_SCALE_harga[laptop['Harga']],
        } for laptop in self.dataDict]

    @property
    def normalized_data(self):
        # x/max [benefit]
        # min/x [cost]
        Merk = [] # max
        Processor = [] # max
        Memori_Internal = [] # max
        RAM = [] # max
        baterai = [] # max
        harga = [] # min
        for data in self.data:
            Merk.append(data['Merk'])
            Processor.append(data['Processor'])
            Memori_Internal.append(data['Memori_Internal'])
            RAM.append(data['RAM'])
            baterai.append(data['Baterai'])
            harga.append(data['Harga'])

        max_Merk = max(Merk)
        max_Processor = max(Processor)
        max_Memori_Internal = max(Memori_Internal)
        max_RAM = max(RAM)
        max_baterai = max(baterai)
        min_harga = min(harga)

        return [
            {   'id': data['id'],
                'Merk': data['Merk']/max_Merk, # benefit
                'Processor': data['Processor']/max_Processor, # benefit
                'Memori_Internal': data['Memori_Internal']/max_Memori_Internal, # benefit
                'RAM': data['RAM']/max_RAM, # benefit
                'Baterai': data['Baterai']/max_baterai, # benefit
                'Harga': min_harga/data['Harga'] # cost
                }
            for data in self.data
        ]
 

class WeightedProduct(BaseMethod):
    def __init__(self, dataDict, setWeight:dict):
        super().__init__(data_dict=dataDict, **setWeight)
    @property
    def calculate(self):
        weight = self.weight
        result = {row['id']:
    round(
        row['Merk'] ** weight['Merk'] *
        row['Processor'] ** weight['Processor'] *
        row['Memori_Internal'] ** weight['Memori_Internal'] *
        row['RAM'] ** weight['RAM'] *
        row['Baterai'] ** weight['Baterai'] *
        row['Harga'] ** weight['Harga']
        , 2
    )
    for row in self.normalized_data}

        #sorting
        # return result
        return dict(sorted(result.items(), key=lambda x:x[1], reverse=True))