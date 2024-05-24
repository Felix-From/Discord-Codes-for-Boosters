import json

class Rarity:
    def __init__(self):
        self.common = 0
        self.uncommon = 1
        self.rare = 2
        self.epic = 3
        self.legendary = 4
        self.RNGESUS = 5

rarity = Rarity()

class Content:
    class Money:
        def __init__(self,MoneyType : str = "Money", Anzahl : int = 0) -> None:
            self.type = 0
            self.MoneyType = MoneyType
            self.Anzahl = Anzahl
            pass 
    class Vehicle:
        def __init__(self,VehicleName : str = "Faggio", Color:str = "Black") -> None:
            self.type=1
            self.VehicleName = VehicleName
            self.Color = Color
            pass
    class Item:
        def __init__(self,Arr_Items: list[str], Arr_Anzahl: list[int]) -> None:
            if len(Arr_Items) <=0:
                raise Exception("Items is empty")
            if len(Arr_Items) != len(Arr_Anzahl):
                raise Exception("Items and Anzahl are not the same length")
            self.type=2
            self.Arr_Items = Arr_Items
            self.Arr_Anzahl = Arr_Anzahl
            pass  
    def __init__(self) -> None:
        self.common=[]
        self.uncommon=[]
        self.rare=[]
        self.epic=[]
        self.legendary=[]
        self.RNGESUS=[]
    def update(self,category,content):
        if category == rarity.common:
            self.common.append(content.__dict__)
            pass
        elif category == rarity.uncommon:
            self.uncommon.append(content.__dict__)
            pass
        elif category == rarity.rare:
            self.rare.append(content.__dict__)
            pass
        elif category == rarity.epic:
            self.epic.append(content.__dict__)
            pass
        elif category == rarity.legendary:
            self.legendary.append(content.__dict__)
            pass
        elif category == rarity.RNGESUS:
            self.RNGESUS.append(content.__dict__)
            pass


        """
        if type(content) == Content.Money:
            self.Moneys.append(content.__dict__)
        elif type(content) == Content.Vehicle:
            self.Vehicles.append(content.__dict__)
        elif type(content) == Content.Item:
            self.Items.append(content.__dict__)
        """


if __name__ == "__main__":
    con = Content()

    #To Create an Entry you need:
    # con.update(RARITY, con.TYPE(Init_Params))
    # for Items those Params need to be arrays

    con.update(rarity.common, con.Money("Money",2000))
    con.update(rarity.common, con.Money("BlackMoney",2000))
    con.update(rarity.common, con.Vehicle("Faggio", "Black"))
    con.update(rarity.common, con.Item(["Bier","Burger"], [10,10]))

    con.update(rarity.uncommon, con.Money("Money",5000))
    con.update(rarity.uncommon, con.Money("BlackMoney",5000))
    con.update(rarity.uncommon, con.Item(["Ketchup","Pommes"], [10,10]))

    con.update(rarity.rare, con.Money("BlackMoney",10000))
    con.update(rarity.rare, con.Money("Money",10000))
    con.update(rarity.rare, con.Item(["Assault_rifle","ammo_ak"], [1,50]))

    con.update(rarity.epic, con.Money("Money",20000))
    con.update(rarity.epic, con.Money("BlackMoney",20000))

    con.update(rarity.legendary, con.Vehicle("Adder", "Red"))

    con.update(rarity.RNGESUS, con.Vehicle("Specter2", "White"))


    with open("content_config.json", "w") as f:
        json.dump(con.__dict__, f, indent=4)
        print("done")
