import pdfplumber
import re
import json

PATH_TO_FILE = "/Users/healthi/Downloads/HARSHITHA.PDF"
END_OF_PAGE = "---End Of Report---"

def pretty(d, indent=0):
   for key, value in d.items():
      print('\t' * indent + str(key))
      if isinstance(value, dict):
         pretty(value, indent+1)
      else:
         print('\t' * (indent+1) + str(value))

pdf = pdfplumber.open(PATH_TO_FILE)
#p0 = pdf.pages[4] #works
page_to_parse = [8, 9]
final_result = {}
header_name = ["CREATININE, SERUM", "LIPID PROFILE", "LIVER FUNCTION TESTS (LFT)",
"UREA - SERUM / PLASMA" ]
test_name = ["CREATININE-SERUM/PLASMA", "CHOLESTEROL", "HDL", "TRIGLYCERIDES",
"LDL", "VLDL", "TOTALCHOLESTEROLHDLCHOLESTEROLRATIO", "BILIRUBINTOTAL",
"ALBUMIN", "A/GRatio", "AST(SGOT)", "ALT(SGPT)", "ALKALINEPHOSPHATASE",
"GAMMAGLUTAMYLTRANSPEPTIDASE", "BILIRUBINCONJUGATED(DIRECT)", "UREA,SERUM" , "URICACID-SERUM"]
header = ""
previous_result = ""
for z in page_to_parse:
    print(z)
    p0 = pdf.pages[z]
    #identify x top co-ordinate from the page and update top in crop(left,top,righty,rightdown)
    if z == 9:
        p0 = p1.crop((6,150,600,800))
    else:
        p0 = p0.crop((6,290,600,800))
    text = p0.extract_text()
    report_list = text.split("\n")
    for i in range(0,len(report_list)):
        if i == END_OF_PAGE:
            break
        result_row = report_list[i]
        if result_row in header_name:
            header = result_row
            final_result[result_row] = {}
            result = {}
            continue
        split_grouping = result_row.split(" ")
        test_match_name = ""
        for ids,j in enumerate(split_grouping):
            print(j)
            result = {}
            test_match_name = test_match_name + j
            values_ref = split_grouping[ids+1:]
            if re.search('^Method' ,test_match_name):
                ref = []
                result["Method"] = split_grouping
                for ids, x in enumerate(split_grouping):
                    if x == "":
                        ref = split_grouping[ids+1:]
                        result["Method"] =" ".join(list(filter(None,split_grouping[:ids+1])))
                        break
                try:
                    final_result[header][previous_result]["reference"] = list(
                        filter(
                            None,
                            final_result[header][previous_result]["reference"] + ref
                        )
                    )
                    final_result[header][previous_result].update(result)
                except KeyError:
                    pass
                break
            if test_match_name in test_name:
                previous_result = test_match_name
                unit = values_ref[-1:]
                values_ref.pop()
                values_ref = list(filter(None, values_ref))
                lab_result = values_ref[:1]
                values_ref.pop(0)
                result[test_match_name] = {"result" : lab_result , "reference" : values_ref , "unit": unit}
                final_result[header].update(result)
                break
print("\n")
pretty(final_result)
r = json.dumps(final_result)
print(r)
