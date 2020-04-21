import json2table
import json

with open("F:\\Balaji\\faqbot\\application\\resources\\Single_FaQ.json") as jsonfile:
    infoFromJson = json.load(jsonfile)
    build_direction = "LEFT_TO_RIGHT"
    table_attributes = {"style": "width:100%"}
    print(json2table.convert(infoFromJson,
                         build_direction=build_direction,
                         table_attributes=table_attributes))
